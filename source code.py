import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json

class FertilizerManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("AgriCare Fertilizers - Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0fdf4')
        
        # Data Storage
        self.inventory = [
            {'id': 1, 'name': 'Urea', 'stock': 500, 'demand': 450, 'price': 300, 'discount': 5},
            {'id': 2, 'name': 'DAP', 'stock': 350, 'demand': 400, 'price': 135, 'discount': 8},
            {'id': 3, 'name': 'NPK 10:26:26', 'stock': 200, 'demand': 180, 'price': 1200, 'discount': 7},
            {'id': 4, 'name': 'Potash', 'stock': 150, 'demand': 200, 'price': 950, 'discount': 6},
            {'id': 5, 'name': 'Zinc Sulphate', 'stock': 100, 'demand': 90, 'price': 450, 'discount': 5}
        ]
        
        self.orders = [
            {'id': 1, 'farmer': 'Rajesh Kumar', 'product': 'Urea', 'quantity': 50, 'status': 'Completed', 'date': '2025-10-15'},
            {'id': 2, 'farmer': 'Priya Sharma', 'product': 'DAP', 'quantity': 30, 'status': 'Pending', 'date': '2025-10-16'},
            {'id': 3, 'farmer': 'Amit Patel', 'product': 'NPK 10:26:26', 'quantity': 20, 'status': 'Processing', 'date': '2025-10-17'}
        ]
        
        self.preorders = [
            {'id': 1, 'farmer': 'Suresh Yadav', 'product': 'Urea', 'quantity': 100, 'delivery_date': '2025-11-01', 'status': 'Confirmed', 'mobile': '9876543210', 'placed_date': '2025-10-10'},
            {'id': 2, 'farmer': 'Meena Devi', 'product': 'DAP', 'quantity': 75, 'delivery_date': '2025-11-15', 'status': 'Pending', 'mobile': '9876543211', 'placed_date': '2025-10-15'},
            {'id': 3, 'farmer': 'Vikram Singh', 'product': 'Potash', 'quantity': 50, 'delivery_date': '2025-10-25', 'status': 'Confirmed', 'mobile': '9876543212', 'placed_date': '2025-10-12'}
        ]
        
        self.feedback = [
            {'id': 1, 'farmer': 'Rajesh Kumar', 'product': 'Urea', 'rating': 5, 'comment': 'Excellent quality, saw great results in my wheat crop', 'date': '2025-10-14'},
            {'id': 2, 'farmer': 'Suresh Yadav', 'product': 'DAP', 'rating': 4, 'comment': 'Good product but delivery was slightly delayed', 'date': '2025-10-13'},
            {'id': 3, 'farmer': 'Meena Devi', 'product': 'Potash', 'rating': 5, 'comment': 'Very effective for my potato crop. Highly recommended!', 'date': '2025-10-12'}
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#15803d', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🌾 AgriCare Fertilizers", 
                              font=('Arial', 20, 'bold'), bg='#15803d', fg='white')
        title_label.pack(side='left', padx=20, pady=15)
        
        subtitle_label = tk.Label(header_frame, text="Smart Demand Management & Pre-Order System", 
                                 font=('Arial', 10), bg='#15803d', fg='#d1fae5')
        subtitle_label.place(x=20, y=50)
        
        # Navigation Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_preorder_tab()
        self.create_inventory_tab()
        self.create_orders_tab()
        self.create_feedback_tab()
        
    def create_dashboard_tab(self):
        dashboard = tk.Frame(self.notebook, bg='#f0fdf4')
        self.notebook.add(dashboard, text='📊 Dashboard')
        
        # Statistics Cards
        stats_frame = tk.Frame(dashboard, bg='#f0fdf4')
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        self.create_stat_card(stats_frame, "Total Products", str(len(self.inventory)), '#16a34a', 0)
        self.create_stat_card(stats_frame, "Pre-Orders", str(len(self.preorders)), '#9333ea', 1)
        self.create_stat_card(stats_frame, "Regular Orders", str(len(self.orders)), '#2563eb', 2)
        avg_rating = sum(f['rating'] for f in self.feedback) / len(self.feedback)
        self.create_stat_card(stats_frame, "Avg Rating", f"{avg_rating:.1f}⭐", '#eab308', 3)
        
        # Demand Analysis
        analysis_frame = tk.LabelFrame(dashboard, text="📈 Demand vs Stock Analysis", 
                                      font=('Arial', 12, 'bold'), bg='white', padx=15, pady=15)
        analysis_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        for item in self.inventory:
            self.create_demand_bar(analysis_frame, item)
            
    def create_stat_card(self, parent, title, value, color, column):
        card = tk.Frame(parent, bg='white', relief='raised', bd=2)
        card.grid(row=0, column=column, padx=10, pady=10, sticky='ew')
        parent.columnconfigure(column, weight=1)
        
        title_label = tk.Label(card, text=title, font=('Arial', 10), bg='white', fg='#6b7280')
        title_label.pack(pady=(10, 5))
        
        value_label = tk.Label(card, text=value, font=('Arial', 24, 'bold'), bg='white', fg=color)
        value_label.pack(pady=(0, 10))
        
    def create_demand_bar(self, parent, item):
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', pady=5)
        
        ratio = item['stock'] / item['demand']
        if ratio < 0.8:
            status = "Low Stock"
            color = '#dc2626'
        elif ratio < 1.2:
            status = "Optimal"
            color = '#16a34a'
        else:
            status = "Overstock"
            color = '#eab308'
        
        header = tk.Frame(frame, bg='white')
        header.pack(fill='x')
        
        name_label = tk.Label(header, text=item['name'], font=('Arial', 10, 'bold'), bg='white')
        name_label.pack(side='left')
        
        status_label = tk.Label(header, text=status, font=('Arial', 8), bg=color, fg='white', padx=8, pady=2)
        status_label.pack(side='right')
        
        info_label = tk.Label(frame, text=f"Stock: {item['stock']} | Demand: {item['demand']} | Ratio: {ratio*100:.0f}%",
                             font=('Arial', 9), bg='white', fg='#6b7280')
        info_label.pack(anchor='w')
        
        # Progress bar
        canvas = tk.Canvas(frame, height=10, bg='#e5e7eb', highlightthickness=0)
        canvas.pack(fill='x', pady=5)
        width = min(ratio * 100, 100)
        canvas.create_rectangle(0, 0, canvas.winfo_reqwidth() * width / 100, 10, fill='#16a34a', outline='')
        
    def create_preorder_tab(self):
        preorder = tk.Frame(self.notebook, bg='#f0fdf4')
        self.notebook.add(preorder, text='📅 Pre-Orders')
        
        # Pre-order Form
        form_frame = tk.LabelFrame(preorder, text="Place Pre-Order (Get up to 8% Discount!)", 
                                   font=('Arial', 12, 'bold'), bg='#7c3aed', fg='white', padx=20, pady=20)
        form_frame.pack(fill='x', padx=20, pady=20)
        
        # Form fields
        fields_frame = tk.Frame(form_frame, bg='#7c3aed')
        fields_frame.pack(fill='x')
        
        tk.Label(fields_frame, text="Farmer Name:", bg='#7c3aed', fg='white', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.preorder_farmer = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.preorder_farmer.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(fields_frame, text="Mobile:", bg='#7c3aed', fg='white', font=('Arial', 10)).grid(row=0, column=2, sticky='w', pady=5)
        self.preorder_mobile = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.preorder_mobile.grid(row=0, column=3, padx=10, pady=5)
        
        tk.Label(fields_frame, text="Product:", bg='#7c3aed', fg='white', font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.preorder_product = ttk.Combobox(fields_frame, font=('Arial', 10), width=23, state='readonly')
        self.preorder_product['values'] = [f"{item['name']} - ₹{item['price']} ({item['discount']}% off)" for item in self.inventory]
        self.preorder_product.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(fields_frame, text="Quantity (bags):", bg='#7c3aed', fg='white', font=('Arial', 10)).grid(row=1, column=2, sticky='w', pady=5)
        self.preorder_quantity = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.preorder_quantity.grid(row=1, column=3, padx=10, pady=5)
        
        tk.Label(fields_frame, text="Delivery Date:", bg='#7c3aed', fg='white', font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.preorder_date = tk.Entry(fields_frame, font=('Arial', 10), width=25)
        self.preorder_date.insert(0, "YYYY-MM-DD")
        self.preorder_date.grid(row=2, column=1, padx=10, pady=5)
        
        submit_btn = tk.Button(fields_frame, text="Submit Pre-Order", command=self.submit_preorder,
                              bg='white', fg='#7c3aed', font=('Arial', 10, 'bold'), padx=20, pady=5)
        submit_btn.grid(row=2, column=3, padx=10, pady=5)
        
        # Pre-orders Table
        table_frame = tk.LabelFrame(preorder, text="Manage Pre-Orders", font=('Arial', 12, 'bold'), 
                                   bg='white', padx=10, pady=10)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scroll = tk.Scrollbar(table_frame)
        scroll.pack(side='right', fill='y')
        
        # Treeview
        self.preorder_tree = ttk.Treeview(table_frame, columns=('ID', 'Farmer', 'Mobile', 'Product', 'Quantity', 'Delivery', 'Placed', 'Status'),
                                         show='headings', yscrollcommand=scroll.set, height=10)
        scroll.config(command=self.preorder_tree.yview)
        
        for col in ('ID', 'Farmer', 'Mobile', 'Product', 'Quantity', 'Delivery', 'Placed', 'Status'):
            self.preorder_tree.heading(col, text=col)
            self.preorder_tree.column(col, width=120)
        
        self.preorder_tree.pack(fill='both', expand=True)
        self.refresh_preorder_table()
        
        # Action buttons
        btn_frame = tk.Frame(table_frame, bg='white')
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(btn_frame, text="✓ Confirm Selected", command=lambda: self.update_preorder_status('Confirmed'),
                 bg='#16a34a', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5).pack(side='left', padx=5)
        tk.Button(btn_frame, text="✗ Reject Selected", command=lambda: self.update_preorder_status('Rejected'),
                 bg='#dc2626', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5).pack(side='left', padx=5)
        
    def create_inventory_tab(self):
        inventory = tk.Frame(self.notebook, bg='#f0fdf4')
        self.notebook.add(inventory, text='📦 Inventory')
        
        table_frame = tk.LabelFrame(inventory, text="Inventory Management", font=('Arial', 12, 'bold'), 
                                   bg='white', padx=10, pady=10)
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        scroll = tk.Scrollbar(table_frame)
        scroll.pack(side='right', fill='y')
        
        inventory_tree = ttk.Treeview(table_frame, columns=('Product', 'Stock', 'Demand', 'Price', 'Discount', 'Status'),
                                     show='headings', yscrollcommand=scroll.set, height=15)
        scroll.config(command=inventory_tree.yview)
        
        for col in ('Product', 'Stock', 'Demand', 'Price', 'Discount', 'Status'):
            inventory_tree.heading(col, text=col)
            inventory_tree.column(col, width=150)
        
        for item in self.inventory:
            ratio = item['stock'] / item['demand']
            status = "Low Stock" if ratio < 0.8 else "Optimal" if ratio < 1.2 else "Overstock"
            inventory_tree.insert('', 'end', values=(
                item['name'],
                f"{item['stock']} bags",
                f"{item['demand']} bags",
                f"₹{item['price']}",
                f"{item['discount']}% OFF",
                status
            ))
        
        inventory_tree.pack(fill='both', expand=True)
        
    def create_orders_tab(self):
        orders = tk.Frame(self.notebook, bg='#f0fdf4')
        self.notebook.add(orders, text='🛒 Orders')
        
        # Order Form
        form_frame = tk.LabelFrame(orders, text="Create New Order", font=('Arial', 12, 'bold'), 
                                  bg='white', padx=20, pady=20)
        form_frame.pack(fill='x', padx=20, pady=20)
        
        fields = tk.Frame(form_frame, bg='white')
        fields.pack()
        
        tk.Label(fields, text="Farmer:", bg='white', font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5)
        self.order_farmer = tk.Entry(fields, font=('Arial', 10), width=20)
        self.order_farmer.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(fields, text="Product:", bg='white', font=('Arial', 10)).grid(row=0, column=2, padx=5, pady=5)
        self.order_product = ttk.Combobox(fields, font=('Arial', 10), width=18, state='readonly')
        self.order_product['values'] = [item['name'] for item in self.inventory]
        self.order_product.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(fields, text="Quantity:", bg='white', font=('Arial', 10)).grid(row=0, column=4, padx=5, pady=5)
        self.order_quantity = tk.Entry(fields, font=('Arial', 10), width=15)
        self.order_quantity.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(fields, text="Add Order", command=self.add_order,
                 bg='#16a34a', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5).grid(row=0, column=6, padx=5, pady=5)
        
        # Orders Table
        table_frame = tk.LabelFrame(orders, text="Recent Orders", font=('Arial', 12, 'bold'), 
                                   bg='white', padx=10, pady=10)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scroll = tk.Scrollbar(table_frame)
        scroll.pack(side='right', fill='y')
        
        self.order_tree = ttk.Treeview(table_frame, columns=('ID', 'Farmer', 'Product', 'Quantity', 'Date', 'Status'),
                                      show='headings', yscrollcommand=scroll.set, height=12)
        scroll.config(command=self.order_tree.yview)
        
        for col in ('ID', 'Farmer', 'Product', 'Quantity', 'Date', 'Status'):
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, width=150)
        
        self.order_tree.pack(fill='both', expand=True)
        self.refresh_order_table()
        
    def create_feedback_tab(self):
        feedback = tk.Frame(self.notebook, bg='#f0fdf4')
        self.notebook.add(feedback, text='💬 Feedback')
        
        # Feedback Form
        form_frame = tk.LabelFrame(feedback, text="Submit Feedback", font=('Arial', 12, 'bold'), 
                                  bg='white', padx=20, pady=20)
        form_frame.pack(fill='x', padx=20, pady=20)
        
        fields = tk.Frame(form_frame, bg='white')
        fields.pack()
        
        tk.Label(fields, text="Farmer Name:", bg='white', font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.feedback_farmer = tk.Entry(fields, font=('Arial', 10), width=30)
        self.feedback_farmer.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(fields, text="Product:", bg='white', font=('Arial', 10)).grid(row=0, column=2, sticky='w', pady=5)
        self.feedback_product = ttk.Combobox(fields, font=('Arial', 10), width=28, state='readonly')
        self.feedback_product['values'] = [item['name'] for item in self.inventory]
        self.feedback_product.grid(row=0, column=3, padx=10, pady=5)
        
        tk.Label(fields, text="Rating:", bg='white', font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.feedback_rating = ttk.Combobox(fields, font=('Arial', 10), width=28, state='readonly')
        self.feedback_rating['values'] = ['5 - Excellent', '4 - Good', '3 - Average', '2 - Poor', '1 - Very Poor']
        self.feedback_rating.current(0)
        self.feedback_rating.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(fields, text="Comment:", bg='white', font=('Arial', 10)).grid(row=2, column=0, sticky='nw', pady=5)
        self.feedback_comment = tk.Text(fields, font=('Arial', 10), width=70, height=4)
        self.feedback_comment.grid(row=2, column=1, columnspan=3, padx=10, pady=5)
        
        tk.Button(form_frame, text="Submit Feedback", command=self.add_feedback,
                 bg='#16a34a', fg='white', font=('Arial', 10, 'bold'), padx=20, pady=8).pack(pady=10)
        
        # Feedback List
        list_frame = tk.LabelFrame(feedback, text="Customer Feedback", font=('Arial', 12, 'bold'), 
                                  bg='white', padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side='right', fill='y')
        
        self.feedback_tree = ttk.Treeview(list_frame, columns=('Farmer', 'Product', 'Rating', 'Comment', 'Date'),
                                         show='headings', yscrollcommand=scroll.set, height=10)
        scroll.config(command=self.feedback_tree.yview)
        
        for col in ('Farmer', 'Product', 'Rating', 'Comment', 'Date'):
            self.feedback_tree.heading(col, text=col)
            if col == 'Comment':
                self.feedback_tree.column(col, width=300)
            else:
                self.feedback_tree.column(col, width=120)
        
        self.feedback_tree.pack(fill='both', expand=True)
        self.refresh_feedback_table()
        
    def submit_preorder(self):
        farmer = self.preorder_farmer.get()
        mobile = self.preorder_mobile.get()
        product = self.preorder_product.get().split(' - ')[0] if self.preorder_product.get() else ''
        quantity = self.preorder_quantity.get()
        delivery_date = self.preorder_date.get()
        
        if not all([farmer, mobile, product, quantity, delivery_date]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!")
            return
        
        new_id = max([p['id'] for p in self.preorders]) + 1 if self.preorders else 1
        self.preorders.append({
            'id': new_id,
            'farmer': farmer,
            'product': product,
            'quantity': quantity,
            'delivery_date': delivery_date,
            'status': 'Pending',
            'mobile': mobile,
            'placed_date': datetime.now().strftime('%Y-%m-%d')
        })
        
        self.refresh_preorder_table()
        messagebox.showinfo("Success", "Pre-order placed successfully!")
        
        # Clear fields
        self.preorder_farmer.delete(0, tk.END)
        self.preorder_mobile.delete(0, tk.END)
        self.preorder_product.set('')
        self.preorder_quantity.delete(0, tk.END)
        
    def add_order(self):
        farmer = self.order_farmer.get()
        product = self.order_product.get()
        quantity = self.order_quantity.get()
        
        if not all([farmer, product, quantity]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!")
            return
        
        new_id = max([o['id'] for o in self.orders]) + 1 if self.orders else 1
        self.orders.append({
            'id': new_id,
            'farmer': farmer,
            'product': product,
            'quantity': quantity,
            'status': 'Pending',
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        
        self.refresh_order_table()
        messagebox.showinfo("Success", "Order added successfully!")
        
        self.order_farmer.delete(0, tk.END)
        self.order_product.set('')
        self.order_quantity.delete(0, tk.END)
        
    def add_feedback(self):
        farmer = self.feedback_farmer.get()
        product = self.feedback_product.get()
        rating = int(self.feedback_rating.get()[0]) if self.feedback_rating.get() else 5
        comment = self.feedback_comment.get("1.0", tk.END).strip()
        
        if not all([farmer, product, comment]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        new_id = max([f['id'] for f in self.feedback]) + 1 if self.feedback else 1
        self.feedback.append({
            'id': new_id,
            'farmer': farmer,
            'product': product,
            'rating': rating,
            'comment': comment,
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        
        self.refresh_feedback_table()
        messagebox.showinfo("Success", "Feedback submitted successfully!")
        
        self.feedback_farmer.delete(0, tk.END)
        self.feedback_product.set('')
        self.feedback_comment.delete("1.0", tk.END)
        
    def update_preorder_status(self, status):
        selected = self.preorder_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a pre-order!")
            return
        
        item = self.preorder_tree.item(selected[0])
        preorder_id = int(item['values'][0])
        
        for preorder in self.preorders:
            if preorder['id'] == preorder_id:
                preorder['status'] = status
                break
        
        self.refresh_preorder_table()
        messagebox.showinfo("Success", f"Pre-order {status.lower()}!")
        
    def refresh_preorder_table(self):
        for item in self.preorder_tree.get_children():
            self.preorder_tree.delete(item)
        
        for preorder in self.preorders:
            self.preorder_tree.insert('', 'end', values=(
                f"#{preorder['id']}",
                preorder['farmer'],
                preorder['mobile'],
                preorder['product'],
                f"{preorder['quantity']} bags",
                preorder['delivery_date'],
                preorder['placed_date'],
                preorder['status']
            ))
            
    def refresh_order_table(self):
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        
        for order in self.orders:
            self.order_tree.insert('', 'end', values=(
                f"#{order['id']}",
                order['farmer'],
                order['product'],
                f"{order['quantity']} bags",
                order['date'],
                order['status']
            ))
            
    def refresh_feedback_table(self):
        for item in self.feedback_tree.get_children():
            self.feedback_tree.delete(item)
        
        for fb in self.feedback:
            self.feedback_tree.insert('', 'end', values=(
                fb['farmer'],
                fb['product'],
                '⭐' * fb['rating'],
                fb['comment'],
                fb['date']
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = FertilizerManagementSystem(root)
    root.mainloop()