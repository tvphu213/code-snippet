from transformers import pipeline
import tqdm

# initialize pipeline
classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
    device=0,
)


candidate_labels = ["politics", "science", "fashion"]


TOTAL = 100
SENTENCE = "This is a test"


def data():
    for i in range(TOTAL):
        yield SENTENCE


print("No batching, streaming")
for result in tqdm.tqdm(classifier(data(), candidate_labels=candidate_labels), total=TOTAL):
    pass
    # print(result)
print("Batching, streaming")
for result in tqdm.tqdm(classifier(data(), candidate_labels=candidate_labels, batch_size=24), total=TOTAL):
    pass
    # print(result)
print("No batching, no streaming")
for i in tqdm.tqdm(range(TOTAL)):
    result = classifier(SENTENCE, candidate_labels=candidate_labels)
    pass
    # print(result)
