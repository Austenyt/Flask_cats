from flask import Flask, render_template, request, redirect, url_for

from models import Cat, Breed, Gender

app = Flask(__name__)


@app.route('/')
def index():
    cats = Cat.select().join(Breed).switch(Cat).join(Gender)
    return render_template('index.html', cats=cats)

@app.route('/add', methods=['GET', 'POST'])
def add_cat():
    if request.method == 'POST':
        name = request.form['name']
        breed = request.form['breed']
        gender = request.form['gender']
        age = request.form['age']
        color = request.form['color']
        weight = request.form['weight']
        temper = request.form['temper']
        print(gender, type(gender))

        Cat.create(
            name=name,
            breed=breed,
            gender=gender,
            age=age,
            color=color,
            weight=weight,
            temper=temper
        )
        return redirect(url_for('index'))
    breeds = Breed.select()
    genders = Gender.select()
    return render_template('add_cat.html', breeds=breeds, genders=genders)

@app.route('/delete/<int:cat_id>', methods=['POST'])
def delete_cat(cat_id):
    cat = Cat.get_or_none(Cat.id == cat_id)
    if cat:
        cat.delete_instance()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
