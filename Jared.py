from flask import Flask, render_template, request, redirect, url_for, flash
import random

app = Flask(__name__)
app.secret_key = 'sheesh'  

VAULT_PASSWORD = 'password'  # Password

tasks = [] # list of data sa mga task

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  
        password = request.form['password']  # Kuhaon ang gi input sa user nga password gikan sa form
        
        if password == VAULT_PASSWORD:  # if ang password og ang vaultpassword is equals
            flash('Login successful!', 'success')  # mag flash og message kung succesful ang paglogin
            return redirect(url_for('dashboard'))  # muadto dayon sa dashboard paghuman og login
        else:
            flash('Invalid password.', 'danger')  # mag flash og message kung mali ang password
    return render_template('login.html')  # mo adto siya sa login

@app.route('/view_tasks')
def view_tasks():
    return render_template('view_tasks.html', tasks=tasks)  # diri tong ishow tanan task na imong gi add

@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':  
        title = request.form['title']  # kuhaon sa form ang gi input sa user na title
        importance = request.form['importance']  # # kuhaon sa form ang gi input sa user na importance
        description = request.form['description']  # # kuhaon sa form ang gi input sa user na description
        
        task_id = len(tasks) + 1  # Mag himo og task_id diria + 1 kay ang index kay mag sugod man sa zero para 1 na mag sugod ang id
        tasks.append({
            'id': task_id,
            'title': title,
            'importance': importance,
            'description': description,
            'status': 'Pending'
        })  # Mao ni diri ang pag add og task
    return render_template('add_task.html')  

@app.route('/update_task', methods=['POST'])
def update_task():
    task_index = int(request.form['task_index'])  # Kuhaon ang task_index sa form
    status = request.form['status']  # Kuhaon ang status sa form
    
    task = next((t for t in tasks if t['id'] == task_index), None)  # pangitaon ang task gamit ang task_index or ang id
    if task:  
        task['status'] = status  # I-update ang status sa task
        return redirect(url_for('view_tasks'))  # redirect dayon sa view_task na route
    else:
        return f"Task {task_index} not found.", 404  # mag flash og message kung walay nakita na task gamit ang task_index

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    random_task = None
    if request.method == 'POST':
        pending_tasks = [t for t in tasks if t['status'] == 'Pending'] # diria kuhaon ra niya ang mga pending na status
        if pending_tasks:
            random_task = random.choice(pending_tasks)  # Mupili og random task pero pending_task ra ang pilion
    return render_template('dashboard.html', random_task=random_task)

if __name__ == "__main__":
    app.run(debug=True)
