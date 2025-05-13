# app/chat.py
def interactive_chat(collection, search_and_answer_fn):
    print("📚 Document QnA System Ready!")
    while True:
        q = input("\n💬 You: ")
        if q.lower() in ["exit", "quit"]:
            break
        try:
            print("🤖 Assistant:")
            search_and_answer_fn(collection, q)
            # ans = search_and_answer_fn(collection, q)
            # print("🤖 Assistant:", ans)
        except Exception as e:
            print("⚠️ Error:", str(e))
