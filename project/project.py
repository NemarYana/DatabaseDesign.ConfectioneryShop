import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

def create_db():
    conn = sqlite3.connect("baza.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'clients' (
            'client_id' integer primary key AUTOINCREMENT,
            'name' TEXT NOT NULL,
            'surname' TEXT NOT NULL,
            'patronymic' TEXT,
            'phone' TEXT NOT NULL,
            'email' TEXT,
            'registration_date' DATE NOT NULL
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'job_titles' (
            'job_title_id' integer primary key AUTOINCREMENT,
            'job_title_name' TEXT NOT NULL
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'employees' (
            'employee_id' integer primary key AUTOINCREMENT,
            'employee_name' TEXT NOT NULL,
            'employee_surname' TEXT NOT NULL,
            'employee_patronymic' TEXT,
            'job_title_id' INTEGER NOT NULL,
            FOREIGN KEY ('job_title_id') REFERENCES 'job_titles'('job_title_id')
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'suppliers' (
            'supplier_id' integer primary key AUTOINCREMENT,
            'supplier_name' TEXT NOT NULL,
            'supplier_phone' TEXT NOT NULL
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'ingredients' (
            'ingredient_id' integer primary key AUTOINCREMENT,
            'ingredient_name' TEXT NOT NULL,
            'unit' TEXT NOT NULL,
            'stock' REAL,
            'supplier_id' INTEGER NOT NULL,
            FOREIGN KEY(supplier_id) REFERENCES 'suppliers'('supplier_id')
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'products' (
            'product_id' integer primary key AUTOINCREMENT,
            'product_name' TEXT NOT NULL,
            'weight' REAL NOT NULL,
            'price' REAL NOT NULL,
            'is_available' INTEGER NOT NULL
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'recipes' (
            'product_id' INTEGER NOT NULL,
            'ingredient_id' INTEGER NOT NULL,
            'quantity_kg' REAL NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(product_id),
            FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id),
            PRIMARY KEY(product_id, ingredient_id)
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'orders' (
            'order_id' integer primary key AUTOINCREMENT,
            'client_id' INTEGER NOT NULL,
            'employee_id' INTEGER NOT NULL,
            'order_date' DATE NOT NULL,
            'status' TEXT NOT NULL,
            FOREIGN KEY('client_id') REFERENCES 'clients'('client_id'),
            FOREIGN KEY('employee_id') REFERENCES 'employees'('employee_id')
        )
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 'order_items' (
            'order_id' INTEGER NOT NULL,
            'product_id' INTEGER NOT NULL,
            'quantity' INTEGER NOT NULL,
            'price_at_purchase' REAL NOT NULL,
            PRIMARY KEY(order_id, product_id),
            FOREIGN KEY('order_id') REFERENCES 'orders'('order_id'),
            FOREIGN KEY('product_id') REFERENCES 'products'('product_id')
        )
        ''')

    cursor.execute("SELECT COUNT(*) FROM clients")
    if cursor.fetchone()[0] == 0:
        with open('clients.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    name = parts[0].strip()
                    surname = parts[1].strip()
                    patronymic = parts[2].strip()
                    phone = parts[3].strip()
                    email = parts[4].strip()
                    date_reg = parts[5].strip()
                    cursor.execute('INSERT INTO `clients` (`name`, `surname`, `patronymic`, `phone`, `email`, `registration_date`) VALUES (?, ?, ?, ?, ?, ?)', 
                                 (name, surname, patronymic if patronymic else None, phone, email if email else None, date_reg))
    
    cursor.execute("SELECT COUNT(*) FROM job_titles")
    if cursor.fetchone()[0] == 0:
        with open('job_titles.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    job_title_name = parts[0].strip()
                    cursor.execute('INSERT OR IGNORE INTO `job_titles` (`job_title_name`) VALUES (?)', (job_title_name,))
    
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    if cursor.fetchone()[0] == 0:
        with open('suppliers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    name = parts[0].strip()
                    phone = parts[1].strip()
                    cursor.execute('INSERT OR IGNORE INTO `suppliers` (`supplier_name`, `supplier_phone`) VALUES (?, ?)', (name, phone))
    
    cursor.execute("SELECT COUNT(*) FROM ingredients")
    if cursor.fetchone()[0] == 0:
        with open('ingredients.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    name = parts[0].strip()
                    unit = parts[1].strip()
                    stock = float(parts[2].strip())
                    supplier_id = int(parts[3].strip())
                    cursor.execute('INSERT OR IGNORE INTO `ingredients` (`ingredient_name`, `unit`, `stock`, `supplier_id`) VALUES (?, ?, ?, ?)', 
                                 (name, unit, stock, supplier_id))
    
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        with open('products.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    name = parts[0].strip()
                    weight = float(parts[1].strip())
                    price = float(parts[2].strip())
                    is_available = int(parts[3].strip())
                    cursor.execute('INSERT OR IGNORE INTO `products` (`product_name`, `weight`, `price`, `is_available`) VALUES (?, ?, ?, ?)', 
                                 (name, weight, price, is_available))
    
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        with open('employees.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    name = parts[0].strip()
                    surname = parts[1].strip()
                    patronymic = parts[2].strip()
                    job_title_id = int(parts[3].strip())
                    cursor.execute('INSERT INTO `employees` (`employee_name`, `employee_surname`, `employee_patronymic`, `job_title_id`) VALUES (?, ?, ?, ?)', 
                                 (name, surname, patronymic if patronymic else None, job_title_id))

    cursor.execute("SELECT COUNT(*) FROM recipes")
    if cursor.fetchone()[0] == 0:
        with open('recipes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    product_id = int(parts[0].strip())
                    ingredient_id = int(parts[1].strip())
                    quantity = float(parts[2].strip())
                    cursor.execute('INSERT OR IGNORE INTO `recipes` (`product_id`, `ingredient_id`, `quantity_kg`) VALUES (?, ?, ?)', 
                                 (product_id, ingredient_id, quantity))

    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        with open('orders.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    client = int(parts[0].strip())
                    employee = int(parts[1].strip())
                    date_reg = parts[2].strip()
                    status = parts[3].strip()
                    cursor.execute('INSERT INTO `orders` (`client_id`, `employee_id`, `order_date`, `status`) VALUES (?, ?, ?, ?)', 
                                 (client, employee, date_reg, status))
    
    cursor.execute("SELECT COUNT(*) FROM order_items")
    if cursor.fetchone()[0] == 0:
        with open('order_items.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    order = int(parts[0].strip())
                    product = int(parts[1].strip())
                    quantity = int(parts[2].strip())
                    price_at_purchase = float(parts[3].strip())
                    cursor.execute('INSERT INTO `order_items` (`order_id`, `product_id`, `quantity`, `price_at_purchase`) VALUES (?, ?, ?, ?)', 
                                 (order, product, quantity, price_at_purchase))
    

    conn.commit()
    conn.close()

class BakeryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Кондитерская")
        self.root.geometry("1100x650")

        self.root.configure(bg='#f5e6d3')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', background='#e8c9a3', padding=[10, 5])
        style.configure('TButton', background='#ffa7d9', font=('Arial', 9, 'bold'))
        style.map('TButton', background=[('active', '#ff8acc')])
        style.configure('Treeview', rowheight=25, font=('Arial', 9))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), background='#ffbee3')
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_clients_tab()
        self.create_employees_tab()
        self.create_products_tab()
        self.create_ingredients_tab()
        self.create_recipes_tab()
        self.create_orders_tab()
        self.create_reports_tab()
        
        self.refresh_all()
    
    def db_query(self, query, params=(), fetch=False):
        conn = sqlite3.connect("baza.db")
        cur = conn.cursor()
        cur.execute(query, params)
        if fetch:
            result = cur.fetchall()
            conn.close()
            return result
        conn.commit()
        conn.close()
        return True
    
    def refresh_all(self):
        self.load_clients()
        self.load_employees()
        self.load_products()
        self.load_ingredients()
        self.load_orders()
        self.load_products_for_recipes()
    
    def create_clients_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Клиенты")
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Добавить", command=self.client_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Редактировать", command=self.client_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.client_delete).pack(side=tk.LEFT, padx=5)
        
        columns = ("ID", "Фамилия", "Имя", "Отчество", "Телефон", "Email", "Дата")
        self.clients_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=120)
        self.clients_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def load_clients(self):
        for row in self.clients_tree.get_children():
            self.clients_tree.delete(row)
        for client in self.db_query("SELECT * FROM clients", fetch=True):
            self.clients_tree.insert("", tk.END, values=client)
    
    def client_add(self):
        dialog = self.create_dialog("Добавление клиента", 
                                   ["Фамилия:", "Имя:", "Отчество:", "Телефон:", "Email:"])
        if dialog.result:
            self.db_query("""INSERT INTO clients (name, surname, patronymic, phone, email, registration_date) 
                           VALUES (?,?,?,?,?,?)""",
                         (dialog.result[1], dialog.result[0], dialog.result[2] or None, 
                          dialog.result[3], dialog.result[4] or None, datetime.now().strftime("%Y-%m-%d")))
            self.load_clients()
            messagebox.showinfo("Успех", "Клиент добавлен")
    
    def client_edit(self):
        selected = self.get_selected(self.clients_tree)
        if not selected: return
        dialog = self.create_dialog("Редактирование клиента",
                                   ["Фамилия:", "Имя:", "Отчество:", "Телефон:", "Email:"],
                                   [selected[1], selected[2], selected[3], selected[4], selected[5]])
        if dialog.result:
            self.db_query("""UPDATE clients SET surname=?, name=?, patronymic=?, phone=?, email=? 
                           WHERE client_id=?""",
                         (dialog.result[0], dialog.result[1], dialog.result[2] or None,
                          dialog.result[3], dialog.result[4] or None, selected[0]))
            self.load_clients()
            messagebox.showinfo("Успех", "Клиент изменен")
    
    def client_delete(self):
        selected = self.get_selected(self.clients_tree)
        if selected and messagebox.askyesno("Удаление", "Удалить клиента?"):
            self.db_query("DELETE FROM clients WHERE client_id=?", (selected[0],))
            self.load_clients()
    
    def create_employees_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Сотрудники")
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Добавить", command=self.emp_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Редактировать", command=self.emp_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.emp_delete).pack(side=tk.LEFT, padx=5)
        
        columns = ("ID", "Фамилия", "Имя", "Отчество", "Должность")
        self.employees_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        for col in columns:
            self.employees_tree.heading(col, text=col)
            self.employees_tree.column(col, width=120)
        self.employees_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def load_employees(self):
        for row in self.employees_tree.get_children():
            self.employees_tree.delete(row)
        data = self.db_query("""SELECT e.employee_id, e.employee_surname, e.employee_name, 
                               e.employee_patronymic, j.job_title_name 
                               FROM employees e JOIN job_titles j ON e.job_title_id = j.job_title_id""", fetch=True)
        for emp in data:
            self.employees_tree.insert("", tk.END, values=emp)
    
    def emp_add(self):
        jobs = [j[0] for j in self.db_query("SELECT job_title_name FROM job_titles", fetch=True)]
        dialog = self.create_dialog("Добавление сотрудника",
                                   ["Фамилия:", "Имя:", "Отчество:", "Должность:"],
                                   combo_fields=[3], combo_values=[jobs])
        if dialog.result:
            job_id = self.db_query("SELECT job_title_id FROM job_titles WHERE job_title_name=?", (dialog.result[3],), fetch=True)[0][0]
            self.db_query("INSERT INTO employees (employee_name, employee_surname, employee_patronymic, job_title_id) VALUES (?,?,?,?)",
                         (dialog.result[1], dialog.result[0], dialog.result[2] or None, job_id))
            self.load_employees()
            messagebox.showinfo("Успех", "Сотрудник добавлен")
    
    def emp_edit(self):
        selected = self.get_selected(self.employees_tree)
        if not selected: return
        jobs = [j[0] for j in self.db_query("SELECT job_title_name FROM job_titles", fetch=True)]
        dialog = self.create_dialog("Редактирование сотрудника",
                                   ["Фамилия:", "Имя:", "Отчество:", "Должность:"],
                                   [selected[1], selected[2], selected[3], selected[4]],
                                   combo_fields=[3], combo_values=[jobs])
        if dialog.result:
            job_id = self.db_query("SELECT job_title_id FROM job_titles WHERE job_title_name=?", (dialog.result[3],), fetch=True)[0][0]
            self.db_query("UPDATE employees SET employee_name=?, employee_surname=?, employee_patronymic=?, job_title_id=? WHERE employee_id=?",
                         (dialog.result[1], dialog.result[0], dialog.result[2] or None, job_id, selected[0]))
            self.load_employees()
            messagebox.showinfo("Успех", "Сотрудник изменен")
    
    def emp_delete(self):
        selected = self.get_selected(self.employees_tree)
        if selected and messagebox.askyesno("Удаление", "Удалить сотрудника?"):
            self.db_query("DELETE FROM employees WHERE employee_id=?", (selected[0],))
            self.load_employees()
    
    def create_products_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Товары")
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Добавить", command=self.prod_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Редактировать", command=self.prod_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.prod_delete).pack(side=tk.LEFT, padx=5)
        
        columns = ("ID", "Название", "Вес (кг)", "Цена (руб)", "Доступен")
        self.products_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=120)
        self.products_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def load_products(self):
        for row in self.products_tree.get_children():
            self.products_tree.delete(row)
        for prod in self.db_query("SELECT * FROM products", fetch=True):
            avail = "Да" if prod[4] else "Нет"
            self.products_tree.insert("", tk.END, values=(prod[0], prod[1], prod[2], prod[3], avail))
    
    def prod_add(self):
        dialog = self.create_dialog("Добавление товара",
                                   ["Название:", "Вес (кг):", "Цена (руб):", "Доступен:"],
                                   combo_fields=[3], combo_values=[["Да", "Нет"]])
        if dialog.result:
            avail = 1 if dialog.result[3] == "Да" else 0
            self.db_query("INSERT INTO products (product_name, weight, price, is_available) VALUES (?,?,?,?)",
                         (dialog.result[0], float(dialog.result[1]), float(dialog.result[2]), avail))
            self.load_products()
            messagebox.showinfo("Успех", "Товар добавлен")
    
    def prod_edit(self):
        selected = self.get_selected(self.products_tree)
        if not selected: return
        dialog = self.create_dialog("Редактирование товара",
                                   ["Название:", "Вес (кг):", "Цена (руб):", "Доступен:"],
                                   [selected[1], selected[2], selected[3], selected[4]],
                                   combo_fields=[3], combo_values=[["Да", "Нет"]])
        if dialog.result:
            avail = 1 if dialog.result[3] == "Да" else 0
            self.db_query("UPDATE products SET product_name=?, weight=?, price=?, is_available=? WHERE product_id=?",
                         (dialog.result[0], float(dialog.result[1]), float(dialog.result[2]), avail, selected[0]))
            self.load_products()
            messagebox.showinfo("Успех", "Товар изменен")
    
    def prod_delete(self):
        selected = self.get_selected(self.products_tree)
        if selected and messagebox.askyesno("Удаление", "Удалить товар?"):
            self.db_query("DELETE FROM products WHERE product_id=?", (selected[0],))
            self.load_products()
    
    def create_ingredients_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Ингредиенты")
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Добавить", command=self.ing_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Редактировать", command=self.ing_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.ing_delete).pack(side=tk.LEFT, padx=5)
        
        columns = ("ID", "Название", "Ед.изм", "Кол-во", "Поставщик")
        self.ingredients_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        for col in columns:
            self.ingredients_tree.heading(col, text=col)
            self.ingredients_tree.column(col, width=120)
        self.ingredients_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def load_ingredients(self):
        for row in self.ingredients_tree.get_children():
            self.ingredients_tree.delete(row)
        data = self.db_query("""SELECT i.ingredient_id, i.ingredient_name, i.unit, i.stock, s.supplier_name 
                               FROM ingredients i JOIN suppliers s ON i.supplier_id = s.supplier_id""", fetch=True)
        for ing in data:
            self.ingredients_tree.insert("", tk.END, values=ing)
    
    def ing_add(self):
        suppliers = [s[0] for s in self.db_query("SELECT supplier_name FROM suppliers", fetch=True)]
        dialog = self.create_dialog("Добавление ингредиента",
                                   ["Название:", "Ед.изм:", "Кол-во:", "Поставщик:"],
                                   combo_fields=[3], combo_values=[suppliers])
        if dialog.result:
            supp_id = self.db_query("SELECT supplier_id FROM suppliers WHERE supplier_name=?", (dialog.result[3],), fetch=True)[0][0]
            self.db_query("INSERT INTO ingredients (ingredient_name, unit, stock, supplier_id) VALUES (?,?,?,?)",
                         (dialog.result[0], dialog.result[1], float(dialog.result[2]), supp_id))
            self.load_ingredients()
            messagebox.showinfo("Успех", "Ингредиент добавлен")
    
    def ing_edit(self):
        selected = self.get_selected(self.ingredients_tree)
        if not selected: return
        suppliers = [s[0] for s in self.db_query("SELECT supplier_name FROM suppliers", fetch=True)]
        dialog = self.create_dialog("Редактирование ингредиента",
                                   ["Название:", "Ед.изм:", "Кол-во:", "Поставщик:"],
                                   [selected[1], selected[2], selected[3], selected[4]],
                                   combo_fields=[3], combo_values=[suppliers])
        if dialog.result:
            supp_id = self.db_query("SELECT supplier_id FROM suppliers WHERE supplier_name=?", (dialog.result[3],), fetch=True)[0][0]
            self.db_query("UPDATE ingredients SET ingredient_name=?, unit=?, stock=?, supplier_id=? WHERE ingredient_id=?",
                         (dialog.result[0], dialog.result[1], float(dialog.result[2]), supp_id, selected[0]))
            self.load_ingredients()
            messagebox.showinfo("Успех", "Ингредиент изменен")
    
    def ing_delete(self):
        selected = self.get_selected(self.ingredients_tree)
        if selected and messagebox.askyesno("Удаление", "Удалить ингредиент?"):
            self.db_query("DELETE FROM ingredients WHERE ingredient_id=?", (selected[0],))
            self.load_ingredients()

    def create_recipes_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Рецепты")

        left = ttk.Frame(tab)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Label(left, text="Продукты:", font=('Arial', 10, 'bold')).pack()
        self.products_list = tk.Listbox(left, height=25)
        self.products_list.pack(fill=tk.BOTH, expand=True)
        self.products_list.bind("<<ListboxSelect>>", self.on_product_select)
        
        right = ttk.Frame(tab)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(right)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Добавить", command=self.recipe_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.recipe_delete).pack(side=tk.LEFT, padx=5)
        
        columns = ("Ингредиент", "Кол-во", "Ед.изм")
        self.recipe_tree = ttk.Treeview(right, columns=columns, show="headings", height=20)
        for col in columns:
            self.recipe_tree.heading(col, text=col)
            self.recipe_tree.column(col, width=150)
        self.recipe_tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.current_product = None
        self.product_ids = {}
    
    def load_products_for_recipes(self):
        self.products_list.delete(0, tk.END)
        self.product_ids = {}
        for pid, name in self.db_query("SELECT product_id, product_name FROM products", fetch=True):
            self.products_list.insert(tk.END, name)
            self.product_ids[name] = pid
    
    def on_product_select(self, event):
        sel = self.products_list.curselection()
        if sel:
            self.current_product = self.products_list.get(sel[0])
            self.load_recipes()
    
    def load_recipes(self):
        for row in self.recipe_tree.get_children():
            self.recipe_tree.delete(row)
        if not self.current_product:
            return
        pid = self.product_ids.get(self.current_product)
        if pid:
            data = self.db_query("""SELECT i.ingredient_name, r.quantity_kg, i.unit 
                                   FROM recipes r JOIN ingredients i ON r.ingredient_id = i.ingredient_id
                                   WHERE r.product_id = ?""", (pid,), fetch=True)
            for ing in data:
                self.recipe_tree.insert("", tk.END, values=ing)
    
    def recipe_add(self):
        if not self.current_product:
            messagebox.showwarning("Ошибка", "Выберите продукт")
            return
        ingredients = [i[0] for i in self.db_query("SELECT ingredient_name FROM ingredients", fetch=True)]
        dialog = self.create_dialog("Добавление ингредиента в рецепт",
                                   ["Ингредиент:", "Количество (кг):"],
                                   combo_fields=[0], combo_values=[ingredients])
        if dialog.result:
            pid = self.product_ids[self.current_product]
            ing_id = self.db_query("SELECT ingredient_id FROM ingredients WHERE ingredient_name=?", (dialog.result[0],), fetch=True)[0][0]
            qty = float(dialog.result[1])
            exists = self.db_query("SELECT 1 FROM recipes WHERE product_id=? AND ingredient_id=?", (pid, ing_id), fetch=True)
            if exists:
                self.db_query("UPDATE recipes SET quantity_kg=? WHERE product_id=? AND ingredient_id=?", (qty, pid, ing_id))
            else:
                self.db_query("INSERT INTO recipes VALUES (?,?,?)", (pid, ing_id, qty))
            self.load_recipes()
            messagebox.showinfo("Успех", "Ингредиент добавлен")
    
    def recipe_delete(self):
        selected = self.recipe_tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите ингредиент")
            return
        ing_name = self.recipe_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Удаление", f"Удалить {ing_name} из рецепта?"):
            pid = self.product_ids[self.current_product]
            ing_id = self.db_query("SELECT ingredient_id FROM ingredients WHERE ingredient_name=?", (ing_name,), fetch=True)[0][0]
            self.db_query("DELETE FROM recipes WHERE product_id=? AND ingredient_id=?", (pid, ing_id))
            self.load_recipes()

    def create_orders_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Заказы")
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Новый заказ", command=self.create_order).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Изменить статус", command=self.change_status).pack(side=tk.LEFT, padx=5)
        
        columns = ("ID", "Клиент", "Сотрудник", "Дата", "Статус")
        self.orders_tree = ttk.Treeview(tab, columns=columns, show="headings", height=20)
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=150)
        self.orders_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.orders_tree.bind("<Double-1>", lambda e: self.view_order())
    
    def load_orders(self):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)
        orders = self.db_query("""SELECT o.order_id, c.surname || ' ' || c.name, 
                                 e.employee_surname || ' ' || e.employee_name, o.order_date, o.status
                                 FROM orders o JOIN clients c ON o.client_id = c.client_id
                                 JOIN employees e ON o.employee_id = e.employee_id
                                 ORDER BY o.order_id DESC""", fetch=True)
        for order in orders:
            self.orders_tree.insert("", tk.END, values=order)
    
    def create_order(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Новый заказ")
        dialog.geometry("600x550")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main = ttk.Frame(dialog, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, text="Клиент:").pack(anchor='w')
        clients = [f"{c[0]} - {c[1]} {c[2]}" for c in self.db_query("SELECT client_id, name, surname FROM clients", fetch=True)]
        client_combo = ttk.Combobox(main, values=clients, width=50)
        client_combo.pack(fill=tk.X, pady=5)

        ttk.Label(main, text="Сотрудник:").pack(anchor='w')
        employees = [f"{e[0]} - {e[1]} {e[2]}" for e in self.db_query("SELECT employee_id, employee_name, employee_surname FROM employees", fetch=True)]
        emp_combo = ttk.Combobox(main, values=employees, width=50)
        emp_combo.pack(fill=tk.X, pady=5)

        ttk.Label(main, text="Товары:").pack(anchor='w', pady=(10,0))

        columns = ("ID", "Товар", "Цена", "Кол-во", "Сумма")
        items_tree = ttk.Treeview(main, columns=columns, show="headings", height=8)
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=100)
        items_tree.pack(fill=tk.BOTH, expand=True, pady=5)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Добавить товар", command=lambda: self.add_order_item(items_tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить товар", command=lambda: self.remove_order_item(items_tree)).pack(side=tk.LEFT, padx=5)

        total_label = ttk.Label(main, text="ИТОГО: 0.00 руб.", font=('Arial', 12, 'bold'))
        total_label.pack(anchor='e', pady=10)

        save_frame = ttk.Frame(main)
        save_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        ttk.Button(save_frame, text="Сохранить заказ", 
                  command=lambda: self.save_order(dialog, client_combo, emp_combo, items_tree, total_label)).pack(side=tk.LEFT, padx=5)
        ttk.Button(save_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def add_order_item(self, items_tree):
        dialog = tk.Toplevel()
        dialog.title("Добавить товар")
        dialog.geometry("400x200")
        dialog.grab_set()
        
        ttk.Label(dialog, text="Товар:").pack(pady=5)
        products = [f"{p[0]} - {p[1]} ({p[2]} руб.)" for p in self.db_query("SELECT product_id, product_name, price FROM products WHERE is_available=1", fetch=True)]
        prod_combo = ttk.Combobox(dialog, values=products, width=40)
        prod_combo.pack(pady=5)
        
        ttk.Label(dialog, text="Количество:").pack(pady=5)
        qty_entry = ttk.Entry(dialog)
        qty_entry.pack(pady=5)
        qty_entry.insert(0, "1")
        
        def add():
            if not prod_combo.get() or not qty_entry.get():
                return
            try:
                qty = int(qty_entry.get())
                if qty <= 0: raise ValueError
            except:
                messagebox.showwarning("Ошибка", "Некорректное количество")
                return
            
            prod_data = prod_combo.get().split(" - ")
            prod_id = int(prod_data[0])
            prod_name = prod_data[1].split(" (")[0]
            price = float(prod_data[1].split("(")[1].split()[0])
            total = price * qty

            for item in items_tree.get_children():
                if items_tree.item(item)["values"][0] == prod_id:
                    values = items_tree.item(item)["values"]
                    new_qty = values[3] + qty
                    new_total = price * new_qty
                    items_tree.item(item, values=(prod_id, prod_name, price, new_qty, new_total))
                    dialog.destroy()
                    self.update_order_total(items_tree)
                    return
            
            items_tree.insert("", tk.END, values=(prod_id, prod_name, price, qty, total))
            dialog.destroy()
            self.update_order_total(items_tree)
        
        ttk.Button(dialog, text="Добавить", command=add).pack(pady=20)
    
    def remove_order_item(self, items_tree):
        selected = items_tree.selection()
        if selected:
            items_tree.delete(selected[0])
            self.update_order_total(items_tree)
    
    def update_order_total(self, items_tree):
        total = 0
        for item in items_tree.get_children():
            total += items_tree.item(item)["values"][4]
        for widget in items_tree.master.winfo_children():
            if isinstance(widget, ttk.Label) and "ИТОГО" in widget.cget("text"):
                widget.config(text=f"ИТОГО: {total} руб.")
    
    def save_order(self, dialog, client_combo, emp_combo, items_tree, total_label):
        if not client_combo.get() or not emp_combo.get():
            messagebox.showwarning("Ошибка", "Выберите клиента и сотрудника")
            return
        if not items_tree.get_children():
            messagebox.showwarning("Ошибка", "Добавьте товары в заказ")
            return
        
        client_id = int(client_combo.get().split(" - ")[0])
        employee_id = int(emp_combo.get().split(" - ")[0])
        order_date = datetime.now().strftime("%Y-%m-%d")
        
        self.db_query("INSERT INTO orders (client_id, employee_id, order_date, status) VALUES (?,?,?,?)",
                     (client_id, employee_id, order_date, "Новый"))
        
        order_id = self.db_query("SELECT last_insert_rowid()", fetch=True)[0][0]
        
        for item in items_tree.get_children():
            values = items_tree.item(item)["values"]
            self.db_query("INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?,?,?,?)",
                         (order_id, values[0], values[3], values[2]))
        
        self.load_orders()
        dialog.destroy()
        messagebox.showinfo("Успех", f"Заказ №{order_id} создан!")
    
    def change_status(self):
        selected = self.get_selected(self.orders_tree)
        if not selected: return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменение статуса")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main = ttk.Frame(dialog, padding=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main, text="Новый статус:").pack()
        status_combo = ttk.Combobox(main, values=["Новый", "Готовится", "Выполнен", "Отменен"], width=20)
        status_combo.pack(pady=10)
        status_combo.set("Выполнен")
        
        def save():
            self.db_query("UPDATE orders SET status=? WHERE order_id=?", (status_combo.get(), selected[0]))
            self.load_orders()
            dialog.destroy()
            messagebox.showinfo("Успех", "Статус обновлен")
        
        ttk.Button(main, text="Сохранить", command=save).pack()
    
    def view_order(self):
        selected = self.get_selected(self.orders_tree)
        if not selected: return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Заказ №{selected[0]}")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main = ttk.Frame(dialog, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        info = f"Клиент: {selected[1]}\nСотрудник: {selected[2]}\nДата: {selected[3]}\nСтатус: {selected[4]}"
        ttk.Label(main, text=info, font=('Arial', 10)).pack(anchor='w', pady=5)

        columns = ("Товар", "Количество", "Цена", "Сумма")
        tree = ttk.Treeview(main, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        items = self.db_query("""SELECT p.product_name, oi.quantity, oi.price_at_purchase, 
                                oi.quantity * oi.price_at_purchase
                                FROM order_items oi JOIN products p ON oi.product_id = p.product_id
                                WHERE oi.order_id = ?""", (selected[0],), fetch=True)
        
        total = 0
        for item in items:
            tree.insert("", tk.END, values=item)
            total += item[3]
        
        ttk.Label(main, text=f"ИТОГО: {total} руб.", font=('Arial', 12, 'bold')).pack(anchor='e')
        ttk.Button(main, text="Закрыть", command=dialog.destroy).pack(pady=10)

    def create_reports_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Отчеты")
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="Топ товаров", command=self.report_top_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Выручка", command=self.report_revenue).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Остатки", command=self.report_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Активные заказы", command=self.report_active_orders).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сотрудник по фамилии", command=self.report_employee_by_surname).pack(side=tk.LEFT, padx=5)
        
        self.report_text = tk.Text(tab, wrap=tk.WORD, height=25)
        self.report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def report_top_products(self):
        data = self.db_query("""SELECT p.product_name, SUM(oi.quantity) as sold
                               FROM order_items oi JOIN products p ON oi.product_id = p.product_id
                               GROUP BY oi.product_id ORDER BY sold DESC LIMIT 5""", fetch=True)
        self.report_text.insert(tk.END, "\nТОП-5 ТОВАРОВ:\n\n")
        for i, (name, sold) in enumerate(data, 1):
            self.report_text.insert(tk.END, f"{i}. {name:<30} - {sold} шт.\n")
    
    def report_revenue(self):
        total = self.db_query("SELECT SUM(quantity * price_at_purchase) FROM order_items", fetch=True)[0][0] or 0
        self.report_text.insert(tk.END, f"\nОБЩАЯ ВЫРУЧКА: {total} руб.\n")
        
        monthly = self.db_query("""SELECT strftime('%Y-%m', o.order_date), SUM(oi.quantity * oi.price_at_purchase)
                                  FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
                                  GROUP BY 1 ORDER BY 1 DESC LIMIT 6""", fetch=True)
        if monthly:
            self.report_text.insert(tk.END, "\nВЫРУЧКА ПО МЕСЯЦАМ:\n")
            for month, profit in monthly:
                self.report_text.insert(tk.END, f"{month}: {profit} руб.\n")
    
    def report_stock(self):
        data = self.db_query("SELECT ingredient_name, stock, unit FROM ingredients ORDER BY stock", fetch=True)
        self.report_text.insert(tk.END, "\nОСТАТКИ ИНГРЕДИЕНТОВ:\n")
        low = []
        for name, stock, unit in data:
            self.report_text.insert(tk.END, f"{name:<25} {stock:>8} {unit}\n")
            if stock < 3:
                low.append(name)
        if low:
            self.report_text.insert(tk.END, f"\nКоличество заканчивающихся ингредиентов: {len(low)}\n")

    def report_active_orders(self):
        data = self.db_query("""SELECT o.order_id, c.surname || ' ' || c.name AS client, e.employee_surname || ' ' || e.employee_name AS employee, o.order_date, o.status,
                  COUNT(oi.product_id) AS items_count,
                  SUM(oi.quantity * oi.price_at_purchase) AS total
                  FROM orders o
                  JOIN clients c ON o.client_id = c.client_id
                  JOIN employees e ON o.employee_id = e.employee_id
                  JOIN order_items oi ON o.order_id = oi.order_id
                  WHERE o.status IN ('Новый', 'Готовится')
                  GROUP BY o.order_id
                  ORDER BY 
                      CASE o.status 
                          WHEN 'Новый' THEN 1 
                          WHEN 'Готовится' THEN 2 
                      END,
                  o.order_date""", fetch=True)
    
        if not data:
            self.report_text.insert(tk.END, "\nНет активных заказов!\n")
            return

        self.report_text.insert(tk.END, "\nАКТИВНЫЕ ЗАКАЗЫ\n")
    
        total_revenue = 0
        for order in data:
            order_id, client, employee, date, status, items, total = order

            self.report_text.insert(tk.END, f"ЗАКАЗ №{order_id}\n")
            self.report_text.insert(tk.END, f"   Клиент: {client}\n")
            self.report_text.insert(tk.END, f"   Сотрудник: {employee}\n")
            self.report_text.insert(tk.END, f"   Дата: {date}\n")
            self.report_text.insert(tk.END, f"   Статус: {status}\n")
            self.report_text.insert(tk.END, f"   Товаров: {items} шт.\n")
            self.report_text.insert(tk.END, f"   Сумма: {total} руб.\n")
            self.report_text.insert(tk.END, "-" * 40 + "\n")
            total_revenue += total
    
        self.report_text.insert(tk.END, f"ИТОГО по активным заказам:\n")
        self.report_text.insert(tk.END, f"Количество заказов: {len(data)}\n")
        self.report_text.insert(tk.END, f"Общая сумма: {total_revenue} руб.\n")

    def report_employee_by_surname(self):
        surname = simpledialog.askstring("Поиск сотрудника", "Введите фамилию сотрудника:")
        if not surname:
            return

        data = self.db_query("""SELECT e.employee_id, e.employee_surname, e.employee_name, e.employee_patronymic, j.job_title_name,
                               COUNT(o.order_id) as orders_count,
                               COALESCE(SUM(oi.quantity * oi.price_at_purchase), 0) as total_revenue
                               FROM employees e
                               LEFT JOIN job_titles j ON e.job_title_id = j.job_title_id
                               LEFT JOIN orders o ON e.employee_id = o.employee_id
                               LEFT JOIN order_items oi ON o.order_id = oi.order_id
                               WHERE e.employee_surname = ?
                               GROUP BY e.employee_id""", (surname,), fetch=True)
    
        if not data:
            self.report_text.insert(tk.END, f"Сотрудник с фамилией '{surname}' не найден\n")
            return
    
        for emp in data:
            emp_id, surname_db, name, patronymic, job_title, orders_count, revenue = emp
            full_name = f"{surname_db} {name} {patronymic if patronymic else ''}".strip()

            self.report_text.insert(tk.END, f"СОТРУДНИК: {full_name}\n")
            self.report_text.insert(tk.END, f"Должность: {job_title}\n")
            self.report_text.insert(tk.END, f"Всего заказов: {orders_count}\n")
            self.report_text.insert(tk.END, f"Общая выручка: {revenue} руб.\n")
            
            if orders_count > 0:
                avg_check = revenue / orders_count
                self.report_text.insert(tk.END, f"Средний чек: {avg_check} руб.\n")

            last_orders = self.db_query("""SELECT o.order_id, o.order_date, o.status,
                                           SUM(oi.quantity * oi.price_at_purchase) as total
                                           FROM orders o
                                           JOIN order_items oi ON o.order_id = oi.order_id
                                           WHERE o.employee_id = ?
                                           GROUP BY o.order_id
                                           ORDER BY o.order_date DESC
                                           LIMIT 5""", (emp_id,), fetch=True)
        
            if last_orders:
                self.report_text.insert(tk.END, "\nПОСЛЕДНИЕ 5 ЗАКАЗОВ:\n")
                for order in last_orders:
                     self.report_text.insert(tk.END, f"Заказ №{order[0]} | {order[1]} | {order[2]} | {order[3]} руб.\n")
    
    def get_selected(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите элемент")
            return None
        return tree.item(selected[0])["values"]
    
    def create_dialog(self, title, labels, default_values=None, combo_fields=None, combo_values=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        main = ttk.Frame(dialog, padding=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        entries = []
        combo_fields = combo_fields or []
        combo_values = combo_values or []
        
        for i, label in enumerate(labels):
            ttk.Label(main, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            
            if i in combo_fields and combo_values:
                idx = combo_fields.index(i)
                entry = ttk.Combobox(main, values=combo_values[idx], width=30)
            else:
                entry = ttk.Entry(main, width=32)
            
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            
            if default_values and i < len(default_values) and default_values[i]:
                entry.insert(0, default_values[i])
            
            entries.append(entry)
        
        dialog.result = None
        
        def on_save():
            dialog.result = [e.get().strip() for e in entries]
            if all(dialog.result[i] for i in range(len(dialog.result)) if i not in combo_fields):
                dialog.destroy()
            else:
                messagebox.showwarning("Ошибка", "Заполните все обязательные поля")
        
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Сохранить", command=on_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.root.wait_window(dialog)
        return dialog

create_db()
root = tk.Tk()
app = BakeryApp(root)
root.mainloop()

