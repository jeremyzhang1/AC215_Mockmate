from transformers import LlamaTokenizer, LlamaForCausalLM


# TODO: rudra to actually return the results of a model query
def output_response(tokenizer_in_use, model_in_use, user_query):
    """
    Generate the output response for a given user query.

    Parameters:
        tokenizer_in_use (Tokenizer): The tokenizer object to be used for converting tensors into text.
        model_in_use (Model): The model object to be used for decoding token IDs to text.
        user_query (str): The user query for which the response needs to be generated.

    Returns:
        str: The response generated for the user query.
    """
    # Converting the pytorch tensors into text
    tokenizer = AutoTokenizer.from_pretrained(f"./model_store/{model_dir_name}")

    # Convert tensor to list of token IDs
    token_ids = tensor.tolist()

    # Decode token IDs to text
    text = tokenizer.decode(token_ids, skip_special_tokens=True)

    return text


def load_model_from_local(local_model_path, named_base_model):
    """
    Load a model from the local file system.

    Args:
        local_model_path (str): The path to the local model directory.
        named_base_model (str): The name of the base model.

    Returns:
        tuple: A tuple containing the tokenizer and the model.
    """
    tokenizer = LlamaTokenizer.from_pretrained(named_base_model)
    model = LlamaForCausalLM.from_pretrained(
        local_model_path,
        load_in_8bit=True,
        device_map="auto",
    )
    return tokenizer, model


if __name__ == "__main__":
    print(
        "Model is currently being loaded into RAM, please wait before inputting queries..."
    )
    trained_model_folder = "trained_model"
    base_model = "openlm-research/open_llama_3b_v2"
    model_path = trained_model_folder
    tokenizer, model = load_model_from_local(model_path, base_model)

    # loop and continuously take user input
    print("Model is ready to accept queries!")
    while True:
        user_query = input("> ")
        model_output = output_response(tokenizer, model, user_query)
        print(model_output)
