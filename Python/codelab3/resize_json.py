import json

src = "/home/epk0930/SKALA/Python/codelab3/yelp_review.json"
dst = "/home/epk0930/SKALA/Python/codelab3/review_min.jsonl"

bad = 0
with open(src, "r", encoding="utf-8") as f, open(dst, "w", encoding="utf-8") as out:
    for line_no, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            bad += 1
            continue

        out.write(json.dumps(
            {
                "review_id": obj.get("review_id"),
                "user_id": obj.get("user_id"),
                "text": obj.get("text"),
            },
            ensure_ascii=False
        ) + "\n")

print("done, bad lines:", bad)
