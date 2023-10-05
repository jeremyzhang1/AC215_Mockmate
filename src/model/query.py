import argparse

# TODO: rudra to actually load the model and return the results

def output_response(tensor, model_dir_name = "falcon7b"):
    # Converting the pytorch tensors into text
    tokenizer = AutoTokenizer.from_pretrained(f"./model_store/{model_dir_name}")
    
    # Convert tensor to list of token IDs
    token_ids = tensor.tolist()

    # Decode token IDs to text
    text = tokenizer.decode(token_ids, skip_special_tokens=True)

    return text



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model Query CLI...")