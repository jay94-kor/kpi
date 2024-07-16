class Project:
    def __init__(self, name, revenue, budget):
        self.name = name
        self.revenue = revenue
        self.budget = budget
        self.profit = self.calculate_profit()
        self.profit_margin = self.calculate_profit_margin()
        self.categories = {}

    def calculate_profit(self):
        return self.revenue - self.budget

    def calculate_profit_margin(self):
        if self.revenue == 0:
            return 0
        return (self.profit / self.revenue) * 100

    def add_category(self, category_name, weight=0):
        if category_name not in self.categories:
            self.categories[category_name] = {"items": [], "weight": weight}

    def add_item_to_category(self, category_name, item_name):
        if category_name in self.categories:
            self.categories[category_name]["items"].append(item_name)
        else:
            self.categories[category_name] = {"items": [item_name], "weight": 0}

    def get_categories(self):
        return list(self.categories.keys())

    def get_items_in_category(self, category_name):
        return self.categories.get(category_name, {}).get("items", [])

    def display_project_info(self):
        return {
            "프로젝트명": self.name,
            "프로젝트 매출": self.revenue,
            "프로젝트 예산": self.budget,
            "이익금": self.profit,
            "이익률": f"{self.profit_margin:.2f}%",
            "카테고리와 항목": self.categories
        }