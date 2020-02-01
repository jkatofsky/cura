from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()

@app.route('/companies/all', methods=['GET'])
def all_companies():

    companies = db.collection("companies")
    cursor = companies.list_documents()

    ret_dict = {"Companies": []}

    for document in cursor:

        ret_dict["Companies"].append(document.get().to_dict())

    return jsonify(ret_dict)


if __name__ == '__main__':
    app.run(debug=True)
