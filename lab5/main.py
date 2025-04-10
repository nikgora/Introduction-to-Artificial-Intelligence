def decision_engine(transition_table, start_state):
    """
    Функція реалізує інтерпретатор дерева рішень.

    Аргументи:
    - transition_table: словник, що містить всі стани та переходи.
    - start_state: початковий стан (ключ у transition_table).
    """
    current_state = start_state

    while True:
        node = transition_table.get(current_state)
        if node is None:
            print("Некоректний стан. Завершення програми.")
            break

        # Якщо вузол містить дію, вважаємо його термінальним (листом)
        if 'action' in node:
            print(f"\nРезультат: {node['action']}")
            break

        # Отримання запитання та варіантів відповіді
        question = node.get('question', "Введіть відповідь:")
        answer = input(question + " ").strip().lower()

        # Перехід за відповіддю користувача
        next_state = node.get(answer)
        if next_state:
            current_state = next_state
        else:
            print("Невірна відповідь. Будь ласка, спробуйте ще раз.\n")


if __name__ == '__main__':
    # Розширене дерево рішень із більшою кількістю вузлів та напрямків аналізу
    decision_tree = {
        "start": {
            "question": "Бажаєте запустити процес аналізу? (yes/no)",
            "yes": "prepare_data",
            "no": "exit"
        },
        "prepare_data": {
            "question": "Чи є у вас необхідні дані для аналізу? (yes/no)",
            "yes": "choose_method",
            "no": "collect_data"
        },
        "collect_data": {
            "action": "Починається збір даних..."
        },
        "choose_method": {
            "question": (
                "Оберіть тип аналізу:\n"
                "1 - Класифікація\n"
                "2 - Регресія\n"
                "3 - Кластеризація\n"
                "4 - Візуалізація даних\n"
                "Ваш вибір (1/2/3/4):"
            ),
            "1": "classification",
            "2": "regression",
            "3": "clustering",
            "4": "visualization"
        },
        # Відгалуження для задач класифікації
        "classification": {
            "question": "Чи бажаєте використати алгоритм SVM для класифікації? (yes/no)",
            "yes": "svm",
            "no": "decision_tree_class"
        },
        "svm": {
            "action": "Запуск алгоритму SVM для класифікації."
        },
        "decision_tree_class": {
            "action": "Запуск алгоритму дерева прийняття рішень для класифікації."
        },
        # Відгалуження для задач регресії
        "regression": {
            "question": "Чи спостерігається лінійна залежність у ваших даних? (yes/no)",
            "yes": "linear_reg",
            "no": "non_linear_reg"
        },
        "linear_reg": {
            "action": "Запуск лінійної регресії."
        },
        "non_linear_reg": {
            "question": "Чи бажаєте використовувати регулізовану регресію?\n(yes - Ridge Regression / no - Поліноміальна регресія): (yes/no)",
            "yes": "ridge_reg",
            "no": "poly_reg"
        },
        "ridge_reg": {
            "action": "Запуск нелінійної регресії з регулізацією (Ridge Regression)."
        },
        "poly_reg": {
            "action": "Запуск поліноміальної регресії."
        },
        # Відгалуження для задач кластеризації
        "clustering": {
            "question": (
                "Оберіть метод кластеризації:\n"
                "1 - K-середніх\n"
                "2 - Ієрархічна кластеризація\n"
                "Ваш вибір (1/2):"
            ),
            "1": "kmeans",
            "2": "hierarchical"
        },
        "kmeans": {
            "action": "Запуск алгоритму K-середніх для кластеризації."
        },
        "hierarchical": {
            "action": "Запуск алгоритму ієрархічної кластеризації."
        },
        # Відгалуження для задач візуалізації
        "visualization": {
            "question": (
                "Оберіть тип візуалізації:\n"
                "1 - Гістограма\n"
                "2 - Лінійний графік\n"
                "3 - Діаграма розсіювання\n"
                "Ваш вибір (1/2/3):"
            ),
            "1": "histogram",
            "2": "line_chart",
            "3": "scatter_plot"
        },
        "histogram": {
            "action": "Побудова гістограми."
        },
        "line_chart": {
            "question": "Чи бажаєте додаткову аналітику до лінійного графіка? (yes/no)",
            "yes": "line_chart_with_analysis",
            "no": "line_chart_simple"
        },
        "line_chart_with_analysis": {
            "action": "Побудова лінійного графіка із додатковою аналітикою."
        },
        "line_chart_simple": {
            "action": "Побудова лінійного графіка."
        },
        "scatter_plot": {
            "action": "Побудова діаграми розсіювання."
        },
        "exit": {
            "action": "Розв'язувач завершив роботу."
        }
    }

    # Запуск машини виведення, починаючи з вузла "start"
    decision_engine(decision_tree, "start")
