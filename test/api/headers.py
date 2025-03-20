class Headers:
    def __init__(self, token):
        self.basic = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }