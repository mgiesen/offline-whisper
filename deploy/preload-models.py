import whisper

models = ["tiny", "base", "small", "medium", "large"]

for model in models:
    print(f"Preloading model {model}...")
    whisper.load_model(model)
