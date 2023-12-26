import tkinter as tk
from tkinter import ttk
import psycopg2


class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление складом")
        self.root.geometry("1000x500")

        # Создаем соединение с базой данных
        self.conn = psycopg2.connect(
            database="postgres",
            user="root",
            password="123",
            host="localhost",
            options="-c search_path=sklad"
        )
        self.cursor = self.conn.cursor()

        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Удалить", command=self.delete_item)
        self.sale_context_menu = self.create_sale_context_menu()

        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        create_menu = tk.Menu(menu_bar, tearoff=0)
        create_menu.add_command(label="Добавить сотрудника", command=self.create_sotrudnik)
        create_menu.add_command(label="Добавить магазин", command=self.create_shop)
        create_menu.add_command(label="Добавить склад", command=self.create_sklad)
        create_menu.add_command(label="Добавить категорию товаров", command=self.create_category)
        create_menu.add_command(label="Добавить продукты в наличии", command=self.create_productsInStock)
        # create_menu.add_command(label="Добавить продукты на складе", command=self.create_productsOnSklad)
        # create_menu.add_command(label="Добавить заказ на склад", command=self.create_orderToSklad)
        # create_menu.add_command(label="Добавить заказ со склада", command=self.create_orderFromSklad)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Список сотрудников", command=self.view_employees)
        view_menu.add_command(label="Список магазинов", command=self.view_shops)
        view_menu.add_command(label="Список складов", command=self.view_sklad)
        view_menu.add_command(label="Список категорий товаров", command=self.view_category)
        view_menu.add_command(label="Список продуктов в наличии", command=self.view_productsInStock)

        sales_menu = tk.Menu(menu_bar, tearoff=0)
        sales_menu.add_command(label="Продать продукт в наличии", command=self.sale_productsInStock)

        menu_bar.add_cascade(label="Создать", menu=create_menu)
        menu_bar.add_cascade(label="Просмотр", menu=view_menu)
        menu_bar.add_cascade(label="Продажи", menu=sales_menu)
        menu_bar.add_command(label="Выход", command=self.root.destroy)

        self.root.config(menu=menu_bar)

    def view_employees(self):
        employee_window = tk.Toplevel(self.root)
        employee_window.title("Список сотрудников")

        employee_tree = ttk.Treeview(employee_window, columns=("", "ID", "Name", "LastName", "Position", "Branch"))
        employee_tree.heading("#0", text="")
        employee_tree.heading("#1", text="ID")
        employee_tree.heading("#2", text="Имя")
        employee_tree.heading("#3", text="Фамилия")
        employee_tree.heading("#4", text="Должность")
        employee_tree.heading("#5", text="Филлиал")
        employee_tree.pack(expand=True, fill=tk.BOTH)

        self.cursor.execute("SELECT * FROM sklad.sotrudniki")

        self.sotrudniki_tree = employee_tree

        sotrudniki_data = self.cursor.fetchall()

        employee_tree.bind("<Button-3>",
                           lambda event, tablename="sotrudniki": self.show_context_menu(event, employee_tree,
                                                                                        tablename))

        for employee in sotrudniki_data:
            employee_tree.insert("", "end", values=(employee[0], employee[1], employee[2], employee[3], employee[4]),
                                 tags=("employee_tag"))

    def view_shops(self):
        shops_window = tk.Toplevel(self.root)
        shops_window.title("Список магазинов")

        shops_tree = ttk.Treeview(shops_window, columns=("", "ID", "Address"))
        shops_tree.heading("#0", text="")
        shops_tree.heading("#1", text="ID")
        shops_tree.heading("#2", text="Адрес")
        shops_tree.pack(expand=True, fill=tk.BOTH)

        self.shops_tree = shops_tree

        self.cursor.execute("SELECT * FROM sklad.shops")

        shops_data = self.cursor.fetchall()
        shops_tree.bind("<Button-3>",
                           lambda event, tablename="shops": self.show_context_menu(event, shops_tree,
                                                                                        tablename))

        for shops in shops_data:
            shops_tree.insert("", "end", values=(shops[0], shops[1]))

    def view_sklad(self):
        sklad_window = tk.Toplevel(self.root)
        sklad_window.title("Список складов")

        sklad_tree = ttk.Treeview(sklad_window, columns=("", "ID", "Address"))
        sklad_tree.heading("#0", text="")
        sklad_tree.heading("#1", text="ID")
        sklad_tree.heading("#2", text="Адрес")
        sklad_tree.pack(expand=True, fill=tk.BOTH)

        self.sklad_tree = sklad_tree

        self.cursor.execute("SELECT * FROM sklad.sklad")

        sklad_data = self.cursor.fetchall()
        sklad_tree.bind("<Button-3>",
                           lambda event, tablename="sklad": self.show_context_menu(event, sklad_tree,
                                                                                        tablename))

        for sklad in sklad_data:
            sklad_tree.insert("", "end", values=(sklad[0], sklad[1]))

    def view_category(self):
        category_window = tk.Toplevel(self.root)
        category_window.title("Список складов")

        category_tree = ttk.Treeview(category_window, columns=("", "ID", "Category Name"))
        category_tree.heading("#0", text="")
        category_tree.heading("#1", text="ID")
        category_tree.heading("#2", text="Название категории")
        category_tree.pack(expand=True, fill=tk.BOTH)

        self.category_tree = category_tree

        self.cursor.execute("SELECT * FROM sklad.category")

        category_data = self.cursor.fetchall()
        category_tree.bind("<Button-3>",
                           lambda event, tablename="category": self.show_context_menu(event, category_tree,
                                                                                        tablename))

        for category in category_data:
            category_tree.insert("", "end", values=(category[0], category[1]))

    def view_productsInStock(self):
        category_window = tk.Toplevel(self.root)
        category_window.title("Список продкутов в наличии")

        productsInStock_tree = ttk.Treeview(category_window, columns=("", "ID", "product name", "price", "description",
                                                               "quantity", "edinicaIzmerenia", "categoryName",
                                                               "shopAddress"))
        productsInStock_tree.heading("#0", text="")
        productsInStock_tree.heading("#1", text="ID")
        productsInStock_tree.heading("#2", text="Название продукта")
        productsInStock_tree.heading("#3", text="Цена")
        productsInStock_tree.heading("#4", text="Описание")
        productsInStock_tree.heading("#5", text="Количество")
        productsInStock_tree.heading("#6", text="Единица измерения")
        productsInStock_tree.heading("#7", text="Название категории")
        productsInStock_tree.heading("#8", text="Адрес магазина")
        productsInStock_tree.pack(expand=True, fill=tk.BOTH)

        self.productsInStock_tree = productsInStock_tree

        self.cursor.execute("SELECT * FROM sklad.productsinstock")

        productsInStock_data = self.cursor.fetchall()
        productsInStock_tree.bind("<Button-3>",
                           lambda event, tablename="productsinstock": self.show_context_menu(event, productsInStock_tree,
                                                                                        tablename))

        for product in productsInStock_data:
            productsInStock_tree.insert("", "end", values=(product[0], product[1], product[2], product[3], product[4],
                                                           product[5], product[6], product[7]))

    def load_sotrudniki_data(self):
        self.cursor.execute("SELECT * FROM sklad.sotrudniki")
        sotrudniki_data = self.cursor.fetchall()

        for item in self.sotrudniki_tree.get_children():
            self.sotrudniki_tree.delete(item)

        for sotrudnik in sotrudniki_data:
            self.sotrudniki_tree.insert("", "end", values=sotrudnik)

    def load_shops_data(self):
        self.cursor.execute("SELECT * FROM sklad.shops")
        shops_data = self.cursor.fetchall()

        for item in self.shops_tree.get_children():
            self.shops_tree.delete(item)

        for shop in shops_data:
            self.shops_tree.insert("", "end", values=shop)

    def load_sklad_data(self):
        self.cursor.execute("SELECT * FROM sklad.sklad")
        sklad_data = self.cursor.fetchall()

        for item in self.sklad_tree.get_children():
            self.sklad_tree.delete(item)

        for sklad in sklad_data:
            self.sklad_tree.insert("", "end", values=sklad)

    def load_category_data(self):
        self.cursor.execute("SELECT * FROM sklad.category")
        category_data = self.cursor.fetchall()

        for item in self.category_tree.get_children():
            self.category_tree.delete(item)

        for category in category_data:
            self.category_tree.insert("", "end", values=category)

    def load_productsInStock(self):
        self.cursor.execute("SELECT * FROM sklad.productsinstock")
        productsInStock_data = self.cursor.fetchall()

        for item in self.productsInStock_tree.get_children():
            self.productsInStock_tree.delete(item)

        for productsInStock in productsInStock_data:
            self.productsInStock_tree.insert("", "end", values=productsInStock)

    def create_sotrudnik(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Добавить сотрудника")

        name_label = ttk.Label(create_window, text="Имя:")
        name_entry = ttk.Entry(create_window)

        last_name_label = ttk.Label(create_window, text="Фамилия:")
        last_name_entry = ttk.Entry(create_window)

        dolzhnost_label = ttk.Label(create_window, text="Должность:")
        dolzhnost_entry = ttk.Entry(create_window)

        fillial_label = ttk.Label(create_window, text="Филиал:")
        fillial_entry = ttk.Entry(create_window)

        name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        dolzhnost_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        dolzhnost_entry.grid(row=2, column=1, padx=10, pady=5)

        fillial_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        fillial_entry.grid(row=3, column=1, padx=10, pady=5)

        def insert_data():
            name = name_entry.get()
            last_name = last_name_entry.get()
            dolzhnost = dolzhnost_entry.get()
            fillial = fillial_entry.get()

            self.cursor.execute(
                "INSERT INTO sklad.sotrudniki (name, lastName, dolzhnost, fillial) VALUES (%s, %s, %s, %s)",
                (name, last_name, dolzhnost, fillial)
            )
            self.conn.commit()

            create_window.destroy()

            self.load_sotrudniki_data()

        submit_button = ttk.Button(create_window, text="Создать", command=insert_data)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_shop(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Добавить магазин")

        address_label = ttk.Label(create_window, text="Адрес:")
        address_entry = ttk.Entry(create_window)

        address_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        address_entry.grid(row=0, column=1, padx=10, pady=5)

        def insert_data():
            address = address_entry.get()

            self.cursor.execute(
                "INSERT INTO sklad.shops (address) VALUES (%s)",
                (address,)
            )
            self.conn.commit()

            create_window.destroy()

            self.load_shops_data()

        submit_button = ttk.Button(create_window, text="Создать", command=insert_data)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_sklad(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Добавить склад")

        address_label = ttk.Label(create_window, text="Адрес:")
        address_entry = ttk.Entry(create_window)

        address_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        address_entry.grid(row=0, column=1, padx=10, pady=5)

        def insert_data():
            address = address_entry.get()

            self.cursor.execute(
                "INSERT INTO sklad.sklad (address) VALUES (%s)",
                (address,)
            )
            self.conn.commit()

            create_window.destroy()

            self.load_sklad_data()

        submit_button = ttk.Button(create_window, text="Создать", command=insert_data)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_productsInStock(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Добавить категорию товаров")

        product_name_label = ttk.Label(create_window, text="Название продукта:")
        product_name_entry = ttk.Entry(create_window)

        price_label = ttk.Label(create_window, text="Цена:")
        price_entry = ttk.Entry(create_window)

        quantity_label = ttk.Label(create_window, text="Количество:")
        quantity_entry = ttk.Entry(create_window)

        edinicaIzmer_label = ttk.Label(create_window, text="Единица измерения:")
        edinicaIzmer_entry = ttk.Entry(create_window)

        description_label = ttk.Label(create_window, text="описание:")
        description_entry = ttk.Entry(create_window)

        category_label = ttk.Label(create_window, text="id категории:")
        category_entry = ttk.Entry(create_window)

        shop_label = ttk.Label(create_window, text="id магазина:")
        shop_entry = ttk.Entry(create_window)

        product_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        product_name_entry.grid(row=0, column=1, padx=10, pady=5)

        price_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        price_entry.grid(row=1, column=1, padx=10, pady=5)

        quantity_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        edinicaIzmer_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        edinicaIzmer_entry.grid(row=3, column=1, padx=10, pady=5)

        description_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        description_entry.grid(row=4, column=1, padx=10, pady=5)

        category_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        category_entry.grid(row=5, column=1, padx=10, pady=5)

        shop_label.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        shop_entry.grid(row=6, column=1, padx=10, pady=5)

        def insert_data():
            product_name = product_name_entry.get()
            price = price_entry.get()
            description = description_entry.get()
            quantity = quantity_entry.get()
            edinicaIzmerenia = edinicaIzmer_entry.get()
            category = category_entry.get()
            shop = shop_entry.get()

            self.cursor.execute(
                "INSERT INTO sklad.productsinstock (productName, price, description, quantity, "
                "edinicaIzmerenia, idCategory, idShop) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (product_name, price, description, quantity, edinicaIzmerenia, category, shop)
            )
            self.conn.commit()

            create_window.destroy()

            self.load_productsInStock()

        submit_button = ttk.Button(create_window, text="Создать", command=insert_data)
        submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    def create_category(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Добавить продукты в наличии")

        category_label = ttk.Label(create_window, text="Название категории:")
        category_entry = ttk.Entry(create_window)

        category_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        category_entry.grid(row=0, column=1, padx=10, pady=5)

        def insert_data():
            category = category_entry.get()

            self.cursor.execute(
                "INSERT INTO sklad.category (categoryName) VALUES (%s)",
                (category,)
            )
            self.conn.commit()

            create_window.destroy()

            self.load_sklad_data()

        submit_button = ttk.Button(create_window, text="Создать", command=insert_data)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def show_context_menu(self, event, treeview, tablename):
        item = self.get_selected_item(treeview)
        if item:
            self.context_menu.post(event.x_root, event.y_root)
            self.selected_item = item
            self.tablename = tablename

    def delete_item(self):
        if hasattr(self, 'selected_item') and hasattr(self, 'tablename'):
            item_id = self.selected_item
            tablename = self.tablename

            if item_id is not None:
                self.conn.commit()
                if tablename == "sotrudniki":
                    self.cursor.execute(f"DELETE FROM sklad.sotrudniki WHERE idSotrudnik = %s", (item_id,))
                    self.load_sotrudniki_data()
                elif tablename == "shops":
                    self.cursor.execute(f"DELETE FROM sklad.shops WHERE idShop = %s", (item_id,))
                    self.load_shops_data()
                elif tablename == "sklad":
                    self.cursor.execute(f"DELETE FROM sklad.sklad WHERE idSklad = %s", (item_id,))
                    self.load_sklad_data()
                elif tablename == "category":
                    self.cursor.execute(f"DELETE FROM sklad.category WHERE idCategory = %s", (item_id,))
                    self.load_productsInStock()

                delattr(self, 'selected_item')
                delattr(self, 'tablename')

    def get_selected_item(self, treeview):
        selected_item = treeview.selection()
        if selected_item:
            return treeview.item(selected_item)['values'][0]
        return None

    def create_sale_window(self, product_id):
        sale_window = tk.Toplevel(self.root)
        sale_window.title("Окно продажи")

        quantity_label = ttk.Label(sale_window, text="Количество:")
        quantity_entry = ttk.Entry(sale_window)
        quantity_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        quantity_entry.grid(row=0, column=1, padx=10, pady=5)

        sell_button = ttk.Button(sale_window, text="Продать",
                                 command=lambda: self.sell_item(product_id, int(quantity_entry.get())))
        sell_button.grid(row=1, column=0, columnspan=2, pady=10)

    def show_sale_context_menu(self, event, treeview, tablename):
        item_id = self.get_selected_item(treeview)
        if item_id:
            self.sale_context_menu.post(event.x_root, event.y_root)
            self.selected_item = item_id
            self.tablename = tablename

    def sell_item(self, product_id, quantity_to_sell):
        print(f"Продано {quantity_to_sell} единиц продукта с ID {product_id}")

        self.cursor.execute("UPDATE sklad.productsinstock SET quantity = quantity - %s WHERE idProduct = %s",
                            (quantity_to_sell, product_id))
        self.conn.commit()

        # Обновляем данные в соответствующем представлении
        self.load_productsInStock()

    def sale_productsInStock(self):
        sale_products_window = tk.Toplevel(self.root)
        sale_products_window.title("Выберите продукт для продажи")

        sale_products_tree = ttk.Treeview(sale_products_window, columns=("", "ID",
                                                                         "product name", "price", "description", "quantity", "edinicaIzmerenia", "categoryName", "shopAddress"))
        sale_products_tree.heading("#0", text="")
        sale_products_tree.heading("#1", text="ID")
        sale_products_tree.heading("#2", text="Название продукта")
        sale_products_tree.heading("#3", text="Цена")
        sale_products_tree.heading("#4", text="Описание")
        sale_products_tree.heading("#5", text="Количество")
        sale_products_tree.heading("#6", text="Единица измерения")
        sale_products_tree.heading("#7", text="Название категории")
        sale_products_tree.heading("#8", text="Адрес магазина")
        sale_products_tree.pack(expand=True, fill=tk.BOTH)

        self.sale_products_tree = sale_products_tree

        self.cursor.execute("SELECT * FROM sklad.productsinstock")

        productsInStock_data = self.cursor.fetchall()
        sale_products_tree.bind("<Button-3>",
                                lambda event, treeview=sale_products_tree: self.show_sale_context_menu(event, treeview, tablename="productsinstock"))

        for product in productsInStock_data:
            sale_products_tree.insert("", "end", values=(product[0], product[1], product[2], product[3], product[4],
                                                           product[5], product[6], product[7]))

    def create_sale_context_menu(self):
        sale_context_menu = tk.Menu(self.root, tearoff=0)

        sale_context_menu.add_command(label="Продать", command=self.sell_selected_item)
        return sale_context_menu

    def sell_selected_item(self):
        if hasattr(self, 'selected_item') and hasattr(self, 'tablename'):
            item_id = self.selected_item
            tablename = self.tablename

            if item_id is not None:
                self.create_sale_window(item_id)

                delattr(self, 'selected_item')
                delattr(self, 'tablename')


if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
