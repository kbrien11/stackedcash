from flask import Flask, request, jsonify
from flask_cors import CORS
from app import User,Job,Review,Booking
from app.util import generate_key


User.dbpath = 'data/stacked.db'



api = Flask(__name__)
CORS(api)

@api.route('/api/create', methods = ['POST'])
def create():
    data = request.get_json()
    if data:
        new_user = User(None,data['email'],data['password'],data['first_name'],data['last_name'],data['company'],data['position'],data['city'],data['salary'])
        new_user.api_key = generate_key()
        print(new_user.api_key)
        new_user.save()
        return jsonify({'status':'success', 'token': new_user.api_key})
    return jsonify({"error":"invalid data"})


@api.route('/api/question/<token>', methods = ['POST'])
def question(token):
    output = User.api_authenticate(token)
    data = request.get_json()
    if output:
        new_user = Job(None,data['department'],data['level'],data['years'],data['happy'],output.company,output.pk)
        new_user.insert()
        print(new_user.level)
        return jsonify({'status':'success',"token":output.api_key})
    return jsonify({"error":"invalid data"})

@api.route('/api/personal/<token>', methods =['GET'])
def personal(token):
    output = User.api_authenticate(token)
    if output:
        result = output.all_for_account(token)
        return jsonify ({"results":result})
    return jsonify({"error":"failed"})

@api.route('/')
def hello():
    return "<h1> Hello Keith </h1>"


@api.route('/api/first_name/<token>', methods =['GET'])
def first_name(token):
    output = User.api_authenticate(token)
    if output:
        result = output.get_name(output.api_key)
        city = output.get_city(output.api_key)
        return jsonify ({"results":result,"city":city})
    return jsonify({"error":"failed"})

@api.route('/api/log', methods =['POST'])
def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = User.signin(email,password)
        print(email,password)
        if user:
            print(user)
            return jsonify({"token": user.api_key})
            print(user.api_key)
        return jsonify({"token": ""})

@api.route('/api/company/<company>/<token>',methods =['GET'])
def company(token,company):
    user = User.api_authenticate(token)
    if user:
        output = user.get_company(company)
        average = user.get_avg_sal(company)
        max_sal = user.get_highest_pos(company)
        data = user.get_search_data(company)
        review = Review.count_reviews(company)
        return jsonify({"output":output,"avg":average,"max":max_sal,"data":data,"review":review})
    return jsonify({"error":"failed"})

@api.route('/api/happy/<company>/<token>',methods =['GET'])
def happy(token,company):
    user = User.api_authenticate(token)
    if user:
        output = user.get_company(company)
        happy = Job.job_happiness(company)
        reviews = Review.count_reviews(company)
        return jsonify({"output":output,"happy":happy,"reviews":reviews})
    return jsonify({"error":"failed"})


@api.route('/api/city/<token>',methods =['GET'])
def city(token):
    user = User.api_authenticate(token)
    if user:
        output = user.get_max_city()
        print(user.city)
        return jsonify({"output":output})
    return jsonify({"error":"failed"})

@api.route('/api/top_five_city/<token>',methods =['GET'])
def five_city(token):
    user = User.api_authenticate(token)
    if user:
        output = user.top_five_cities()
        companies = user.highest_paid_companies_in_your_city(user.city)
        positions = user.top_five_positions()
        
        print(user.city)
        return jsonify({"output":output,"results":companies,"positions":positions})
    return jsonify({"error":"failed"})

@api.route('/api/top_five_happy_companies/<token>',methods =['GET'])
def happy_companies(token):
    user = User.api_authenticate(token)
    if user:
        output =Job.top_five_happy_companies()
        
        return jsonify({"output":output})
    return jsonify({"error":"failed"})

@api.route('/api/get_dep_level/<company>/<token>',methods =['GET'])
def get_dep_level(token,company):
    user = User.api_authenticate(token)
    if user:
        output =Job.get_dep_level(company)
        return jsonify({"output":output})
    return jsonify({"error":"failed"})

@api.route('/api/add_review/<token>/<company>', methods = ['POST'])
def review(token,company):
    user = User.api_authenticate(token)
    if user:
        data = request.get_json()
        new_review = Review(None,data['review'],company,data['time_stamp'],data['pros'],data['cons'],user.pk)
        new_review.save()
        return jsonify({"token":user.api_key})
    return jsonify({"token":""})

@api.route('/api/booking/<token>', methods =['POST'])
def booking(token):
    user = User.api_authenticate(token)
    if user:
        data = request.get_json()
        date = request.get_json()['date_stamp']
        time = request.get_json()['time_stamp']
        full = request.get_json()['full_date']
        new_booking = Booking(None,user.first_name,date,time,full,user.pk)
        if new_booking:
           new_booking.save()
        return jsonify({"booking":new_booking.time_stamp})
    return jsonify({"error":"failed"})

@api.route('/api/update_booking/<token>/<pk>', methods =['POST'])
def update_booking(token,pk):
    user = User.api_authenticate(token)
    if user:
        output = request.get_json()
        data = Booking.all_bookings_pk(pk)
        output = Booking(output['pk'],data.first_name,output['date_stamp'],output['time_stamp'],output['full_date'],data.users_pk)
        output.save()
        return jsonify({"booking":output.date_stamp})
    return jsonify({"error":"failed"})

@api.route('/api/get_booking/<token>', methods =['GET'])
def get_booking(token):
    user = User.api_authenticate(token)
    if user:
        output = Booking.get_booking(user.pk)
        results = Booking.all_bookings()
        if output:
            return jsonify({"bookings":output,"results":results})
    return jsonify({"error":"failed"})

@api.route('/api/delete/booking/<token>', methods =['POST'])
def delete_booking(token):
    data = request.get_json()
    if data:
        pk = data['pk']
        output = Booking.remove_booking(pk)
        return jsonify({"message":"success"})
    return jsonify({"message":"failed"})

@api.route('/api/reviews_company/<company>/<token>', methods =['GET'])
def company_review(company,token):
    user = User.api_authenticate(token)
    if user:
        reviews = Review.get_reviews(company)
        return jsonify({"reviews":reviews})
    return jsonify({"error":"failed"})

@api.route('/api/positions/<company>/<token>', methods =['GET'])
def positions(company,token):
    user = User.api_authenticate(token)
    if user:
        positions = User.positions(company)
        return jsonify({"positions":positions})
    return jsonify({"error":"failed"})

if __name__=="__main__":
    api.run(threaded=true, debug=True)
