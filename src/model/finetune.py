import argparse
import pickle
from peft import LoraConfig, get_peft_model
from transformers import (
    LlamaTokenizer,
    LlamaForCausalLM,
    TrainingArguments,
    BitsAndBytesConfig,
    Trainer,
)
import torch
from torch.utils.data import IterableDataset, random_split


class ConstantLengthDataset(IterableDataset):
    """
    Iterable dataset that returns constant length chunks of tokens from stream of text files.
        Args:
            tokenizer (Tokenizer): The processor used for proccessing the data.
            dataset (dataset.Dataset): Dataset with text files.
            infinite (bool): If True the iterator is reset after dataset reaches end else stops.
            seq_length (int): Length of token sequences to return.
            num_of_sequences (int): Number of token sequences to keep in buffer.
            chars_per_token (int): Number of characters per token used to estimate number of tokens in text buffer.
    """

    def __init__(
        self,
        tokenizer,
        dataset,
        infinite=False,
        seq_length=1024,
        num_of_sequences=1024,
        chars_per_token=2.95,
    ):
        """
        Initializes a new instance of the class.

        Parameters:
            tokenizer (Tokenizer): The tokenizer to use for tokenizing the dataset.
            dataset (Dataset): The dataset to process.
            infinite (bool, optional): Whether to loop infinitely over the dataset. Defaults to False.
            seq_length (int, optional): The maximum sequence length. Defaults to 1024.
            num_of_sequences (int, optional): The number of sequences to generate. Defaults to 1024.
            chars_per_token (float, optional): The average number of characters per token. Defaults to 2.95.

        Returns:
            None
        """
        self.tokenizer = tokenizer
        self.concat_token_id = (
            tokenizer.eos_token_id if tokenizer.eos_token_id else 49152
        )
        self.dataset = dataset
        self.seq_length = seq_length
        self.infinite = infinite
        self.current_size = 0
        self.max_buffer_size = seq_length * chars_per_token * num_of_sequences
        self.content_field = "prompt"

    def __iter__(self):
        """
        Returns an iterator object that iterates over the elements of the dataset.

        This function initializes an iterator object using the `iter` function and the `self.dataset` attribute. It then enters a loop that continues until there are no more examples to iterate over. Within this loop, it initializes a buffer and a buffer length variable to store the examples. It continues to append examples to the buffer until the buffer length exceeds the `self.max_buffer_size` threshold or there are no more examples in the iterator. If the buffer length exceeds the threshold, the loop breaks. If there are no more examples in the iterator, it checks if the `self.infinite` attribute is set to `True`. If it is, it reinitializes the iterator using the `iter` function and the `self.dataset` attribute. If it is not, it sets the `more_examples` variable to `False` and breaks out of the loop.

        After constructing the buffer, it tokenizes the inputs using the `self.tokenizer` function with the `truncation` parameter set to `False` and retrieves the `input_ids` from the tokenized inputs. It then initializes an empty list, `all_token_ids`, to store all the token IDs. It iterates over the tokenized inputs and extends the `all_token_ids` list with each tokenized input plus the `self.concat_token_id` attribute.

        After constructing the `all_token_ids` list, it enters another loop that iterates over the `all_token_ids` list in chunks of size `self.seq_length`. It retrieves a chunk of `self.seq_length` token IDs from the `all_token_ids` list and checks if the length of the chunk is equal to `self.seq_length`. If it is, it increments the `self.current_size` attribute by 1 and yields a dictionary containing the `input_ids` and `labels` tensors, both initialized with the chunk of token IDs as `torch.LongTensor` objects.

        The yielded dictionaries represent examples from the dataset and are returned by the iterator object.
        """
        iterator = iter(self.dataset)
        more_examples = True
        while more_examples:
            buffer, buffer_len = [], 0
            while True:
                if buffer_len >= self.max_buffer_size:
                    break
                try:
                    buffer.append(next(iterator)[self.content_field])
                    buffer_len += len(buffer[-1])
                except StopIteration:
                    if self.infinite:
                        iterator = iter(self.dataset)
                    else:
                        more_examples = False
                        break
            tokenized_inputs = self.tokenizer(buffer, truncation=False)["input_ids"]
            all_token_ids = []
            for tokenized_input in tokenized_inputs:
                all_token_ids.extend(tokenized_input + [self.concat_token_id])
            for i in range(0, len(all_token_ids), self.seq_length):
                input_ids = all_token_ids[i : i + self.seq_length]
                if len(input_ids) == self.seq_length:
                    self.current_size += 1
                    yield {
                        "input_ids": torch.LongTensor(input_ids),
                        "labels": torch.LongTensor(input_ids),
                    }


def load_training_data(path):
    """
    Load training data from a file.

    Parameters:
        path (str): The path to the file containing the training data.

    Returns:
        The first element of the loaded data.
    """
    with open(path, "rb") as f:
        res = pickle.load(f)
        return res[0]


def do_train_test_split(loaded_dataset):
    """
    Splits a dataset into a training set and a validation set.

    Parameters:
        dataset (Dataset): The dataset to split.

    Returns:
        Tuple[Dataset, Dataset]: A tuple containing the training set and the validation set.
    """
    train_size = int(0.8 * len(loaded_dataset))
    valid_size = len(loaded_dataset) - train_size
    return random_split(loaded_dataset, [train_size, valid_size])


def do_train_finetune(base_model_for_training, args, train_tensor, eval_tensor):
    """
    Trains a finetuned model using the given base model for training.

    Args:
        base_model_for_training (Model): The base model used for training.
        args (dict): A dictionary of arguments for training.
        train_tensor (Tensor): The tensor containing the training data.
        eval_tensor (Tensor): The tensor containing the evaluation data.

    Returns:
        Trainer: The trained model trainer.

    """
    train_tensor.start_iteration = 0
    trainer = Trainer(
        model=base_model_for_training,
        args=args,
        train_dataset=train_tensor,
        eval_dataset=eval_tensor,
    )
    trainer.train()
    return trainer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Fine-tuning CLI...")
    training_data_folder = "training_data"
    trained_model_folder = "trained_model"

    # load in base model
    base_model = "openlm-research/open_llama_3b_v2"
    tokenizer = LlamaTokenizer.from_pretrained(base_model)
    tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    model = LlamaForCausalLM.from_pretrained(
        base_model,
        load_in_8bit=True,
        device_map="auto",
        quantization_config=nf4_config,
    )

    # configure LoRA
    target_modules = [
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "down_proj",
        "up_proj",
        "lm_head",
    ]
    lora_config = LoraConfig(
        r=16,
        target_modules=target_modules,
        lora_alpha=8,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # training args
    per_device_train_batch_size = 4
    gradient_accumulation_steps = 4
    optim = "adamw_hf"
    learning_rate = 1e-5
    max_grad_norm = 0.3
    warmup_ratio = 0.03
    lr_scheduler_type = "linear"
    training_args = TrainingArguments(
        output_dir=trained_model_folder,
        dataloader_drop_last=True,
        gradient_checkpointing=True,
        gradient_accumulation_steps=gradient_accumulation_steps,
        optim=optim,
        evaluation_strategy="steps",
        max_steps=10,
        eval_steps=10,
        save_steps=10,
        logging_steps=10,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=1,
        learning_rate=learning_rate,
        lr_scheduler_type=lr_scheduler_type,
        warmup_steps=100,
        warmup_ratio=warmup_ratio,
        weight_decay=0.05,
        max_grad_norm=max_grad_norm,
        fp16=True,
    )

    # handle training data
    dataset = load_training_data(training_data_folder + "/ready.pkl")
    train_dataset, valid_dataset = do_train_test_split(dataset)
    train_ds = ConstantLengthDataset(
        tokenizer, train_dataset, infinite=True, seq_length=1024
    )
    valid_ds = ConstantLengthDataset(
        tokenizer, valid_dataset, infinite=False, seq_length=1024
    )
    trainer = do_train_finetune(model, training_args, train_ds, valid_ds)
    trainer.save_model(trained_model_folder)
