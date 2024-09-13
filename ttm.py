import torch
from transformers import BartTokenizer, BartForConditionalGeneration

# Load the BART model and tokenizer
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def summarize_text(text):
    # Encode the text
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)

    # Generate summary
    summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Example usage
if __name__ == "__main__":
    # Sample text to summarize
    text = """
    The BART model is a denoising autoencoder for pretraining sequence-to-sequence models. 
    It can be used for various natural language processing tasks such as text summarization, 
    machine translation, and text generation. BART combines the strengths of BERT and GPT by 
    using a bidirectional encoder and an autoregressive decoder. This allows it to learn rich 
    contextual representations and generate coherent sequences effectively. The model can 
    be fine-tuned on specific tasks to achieve state-of-the-art performance.
    """

    # Get the summary
    summary = summarize_text(text)
    print("Original Text:\n", text)
    print("\nSummary:\n", summary)
