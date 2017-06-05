from flask import Flask, render_template, jsonify
app = Flask(__name__)


@app.route("/")
@app.route("/catalog/")
def catalog_index():
    return None


@app.route("/catalog.json")
def catalog_endpoint():
    categories = [{"id": 1}, {"id": 2}, {"id": 3}]
    return jsonify(category=categories)


@app.route("/catalog/<int:category_id>/")
def category_index(category_id):
    return None


@app.route("/catalog/<int:category_id>/add/")
def category_item_add(category_id):
    return None


@app.route("/catalog/<int:category_id>/<int:item_id>/")
def category_item_show(category_id, item_id):
    return None


@app.route("/catalog/<int:category_id>/<int:item_id>/edit/")
def category_item_edit(category_id, item_id):
    return None


@app.route("/catalog/<int:category_id>/<int:item_id>/delete/")
def category_item_delete(category_id, item_id):
    return None


if __name__ == "__main__":
    app.run(host="127.0.0.1",
            port=8000,
            debug=True)
