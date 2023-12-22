from itertools import count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import Usersform
import MySQLdb
import datetime


db = MySQLdb.connect("127.0.0.1","root","MILTONalmonds@100","vms_db" )

def home(request):
    return render(request,"index.html")

def studentLogin(request):
    try:
        if request.method=="POST":
            cid = request.POST.get("cid")
            # print(cid)
            c_password = request.POST.get("c_password")
            cursor = db.cursor()
            cursor.execute(f"select * from customer where cid='{cid}'")
            data = cursor.fetchone()
            if(c_password==data[5]):
                print(data)
                request.session['cid'] = cid
                return redirect('/student-login/dashboard/')
    except Exception as e:
        print("Exception:",e)
    return render(request,"studentLogin.html")

def studentDashboard(request):
    try:
        if request.session.has_key('cid'):
            id1 = request.session['cid']
            print("id1 = ", id1)
            return render(request,"studentDashboard.html")
    except Exception as e:
        print("Exception:",e)
        return render(request,"studentDashboard.html")

def studentOutlet(request):
    return render(request,"studentOutlet.html")

def studentExpense(request):
    return render(request,"studentExpense.html")

def studentCurrentOrders(request):
    return render(request,"studentCurrentOrders.html")

def studentPastOrders(request):
    return render(request,"studentPastOrders.html")

def studentPastOrderDetails(request):
    return render(request,"studentPastOrderDetails.html")

def studentCart(request):
    return render(request,"studentCart.html")

def vendorLogin(request):
    try:
        if request.method=="POST":
            vid = request.POST.get("vid")
            print(vid)
            v_password = request.POST.get("v_password")
            cursor = db.cursor()
            cursor.execute(f"select * from vendor where vid = '{vid}'")
            data = cursor.fetchone()
            if(v_password==data[7]):
                print(data)
                request.session['vid'] = vid
                return redirect('/vendor-login/dashboard/')
    except Exception as e:
        print("Exception1:",e)
    return render(request,"vendorLogin.html")

def vendorDashboard(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            if request.method == 'POST':
                if 'turn_on' in request.POST:
                    cursor0 = db.cursor()
                    cursor0.execute(f"update item set item_availability = 1 where item_id = '{request.POST.get('turn_on')}'")
                    db.commit()
                elif 'turn_off' in request.POST:
                    cursor0 = db.cursor()
                    cursor0.execute(f"update item set item_availability = 0 where item_id = '{request.POST.get('turn_off')}'")
                    db.commit()
            cursor1 = db.cursor()
            cursor1.execute(f"select count(*) from item where vid = '{vid}' and deleted = 0")
            cursor2 = db.cursor()
            cursor2.execute(f"select item_name, item_availability, item_id from item where vid = '{vid}' and deleted = 0")
            cursor3 = db.cursor()
            cursor3.execute(f"select open from vendor where vid = '{vid}' and deleted = 0")
            open = cursor3.fetchone()[0]
            item_id = dict()
            for i in range(cursor1.fetchone()[0]):
                x = cursor2.fetchone()
                item_id[x[2]] = [x[0], x[1]]
            print(item_id)
            data = {
                'vid':vid,
                'item_id':item_id,
                'open':open,
                }
            return render(request,"vendorDashboard.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorDashboard.html")

def vendorEditItem(request, item_id):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            if request.method == 'POST':
                new_item_name = request.POST.get('itemname')
                new_price = request.POST.get('price')
                cursor0 = db.cursor()
                cursor0.execute(f"update item set item_name = '{new_item_name}', item_price = {new_price} where item_id = '{item_id}'")
                db.commit()
                return redirect('/vendor-login/dashboard/')
            cursor1 = db.cursor()
            cursor1.execute(f"select item_name, item_price from item where item_id = '{item_id}'")
            x = cursor1.fetchone()
            data = {
                'vid':vid,
                'item_id':item_id,
                'item_name':x[0],
                'item_price':x[1],
                }
            return render(request,"vendorEditItem.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorEditItem.html")

def vendorDeleteItem(request, item_id):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            if request.method == 'POST':
                cursor0 = db.cursor()
                cursor0.execute(f"update item set deleted = 1 where item_id = '{item_id}'")
                db.commit()
                return redirect('/vendor-login/dashboard/')
            cursor1 = db.cursor()
            cursor1.execute(f"select item_name, item_price from item where item_id = '{item_id}'")
            x = cursor1.fetchone()
            data = {
                'vid':vid,
                'item_id':item_id,
                'item_name':x[0],
                'item_price':x[1],
                }
            return render(request,"vendorDeleteItem.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorDeleteItem.html")

def vendorAddItem(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            data = {
                'vid':vid,
                }
            if request.method == "POST":
                cursor1 = db.cursor()
                cursor2 = db.cursor()
                itemname = request.POST.get('itemname')
                price = request.POST.get('price')
                
                cursor1.execute(f"select count(*) from item where vid='{vid}'")
                count = cursor1.fetchone()[0]
                item_id = vid + str(count)
                cursor2.execute(f"insert into item values('{item_id}', '{vid}', '{itemname}', {price}, {1}, {0})")
                db.commit()
            return render(request,"vendorAddItem.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorAddItem.html")

def vendorCurrentOrders(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor2 = db.cursor()
            cursor3 = db.cursor()
            cursor1.execute(f"select * from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=0")
            cursor2.execute(f"select count(*) from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=0")
            count = cursor2.fetchone()[0]
            dict1 = dict()
            
            for i in range(count):
                x = cursor1.fetchone()
                oid = x[1]
                items = dict()
                
                if oid in dict1.keys():
                    dict1[oid][0] += x[5]*x[2]
                    cursor3.execute(f"select item_name from item where item_id='{x[0]}' and vid='{vid}'")
                    item_name = cursor3.fetchone()[0]
                    dict1[oid][3][item_name] = x[2]
                else:
                    date = x[12].strftime("%x")
                    time = x[12].strftime("%X")
                    amount = x[5]*x[2]
                    cursor3.execute(f"select item_name from item where item_id='{x[0]}' and vid='{vid}'")
                    item_name = cursor3.fetchone()[0]
                    items[item_name] = x[2]
                    dict1[oid] = [amount, date, time, items]
            print(dict1)

            data = {
                'vid':vid,
                'orders':dict1
                }
            print(data)
            return render(request,"vendorCurrentOrders.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorCurrentOrders.html")

def vendorCurrentOrdersPrepared(request, oid):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor1.execute(f"update orders set is_prepared_flag = 1 where oid = '{oid}'")
            db.commit()
            data = {
                'vid':vid,
            }
            return redirect('/vendor-login/dashboard/current-orders')
    except Exception as e:
        print("Exception2:",e)
        return redirect('/vendor-login/dashboard/current-orders')

def vendorPastOrders(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor2 = db.cursor()
            cursor1.execute(f"select orders.oid, order_item_price, quantity, date_time from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=1")
            cursor2.execute(f"select count(*) from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=1")
            count = cursor2.fetchone()[0]
            dict1 = dict()
            income = 0
            for i in range(count):
                x = cursor1.fetchone()
                oid = x[0]
                
                if oid in dict1.keys():
                    dict1[oid][0] += x[1]*x[2]
                else:
                    date = x[3].strftime("%x")
                    time = x[3].strftime("%X")
                    amount = x[1]*x[2]
                    income += amount
                    dict1[oid] = [amount, date, time]
            
            cursor3 = db.cursor()
            cursor3.execute(f"update vendor set v_income = {income} where vid='{vid}'")
            db.commit()

            data = {
                'vid':vid,
                'orders':dict1
                }
            print(data)
            return render(request,"vendorPastOrders.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorPastOrders.html")

def vendorPastOrderDetails(request, oid):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor1.execute(f"select orders.item_id, item_name, order_item_price, quantity, date_time from item, cart_item, orders where item.item_id = cart_item.item_id and cart_item.oid = orders.oid and orders.item_id = cart_item.item_id and orders.oid = '{oid}'")
            cursor2 = db.cursor()
            cursor2.execute(f"select count(*) from item, cart_item, orders where item.item_id = cart_item.item_id and cart_item.oid = orders.oid and orders.item_id = cart_item.item_id and orders.oid = '{oid}'")
            count = cursor2.fetchone()[0]
            items = dict()
            amount = 0
            for i in range(count):
                x = cursor1.fetchone()
                items[x[0]] = [x[1], x[2], x[3], x[2]*x[3]]
                amount += x[2]*x[3]
            data = {
                'vid':vid,
                'oid':oid,
                'items': items,
                'date' : x[4].strftime("%x"),
                'time' : x[4].strftime("%X"),
                'amount' : amount,
                'count' : count,
                }
            return render(request,"vendorPastOrderDetails.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorPastOrderDetails.html")

def vendorIncome(request):
    try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            cursor1 = db.cursor()
            cursor2 = db.cursor()
            cursor3 = db.cursor()
            cursor1.execute(f"select * from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=1")
            cursor2.execute(f"select count(*) from cart_item left join orders on cart_item.item_id = orders.item_id and cart_item.oid = orders.oid where vid = '{vid}' and is_prepared_flag=1")
            cursor3.execute(f"select shop_name from vendor where vid = '{vid}'")
            count = cursor2.fetchone()[0]
            income = 0
            for i in range(count):
                x = cursor1.fetchone()
                income+=x[5]*x[2]

            data = {
                'vid':vid,
                'income':income,
                'name': cursor3.fetchone()[0]
                }
            return render(request,"vendorIncome.html",data)
    except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorIncome.html")

def vendorShopStatus(request,status):
     try:
        if request.session.has_key('vid'):
            vid = request.session['vid']
            print(status)
            cursor1 = db.cursor()
            cursor1.execute(f"update vendor set open = {status} where vid = '{vid}'")
            return redirect("/vendor-login/dashboard/")
     except Exception as e:
        print("Exception2:",e)
        return render(request,"vendorDashboard.html")

def tempUserform(request):
    finalans = 0
    fn = Usersform()
    data = {'form':fn}
    try:
        if request.method == 'POST':
            n1 = int(request.POST.get('num1'))
            n2 = int(request.POST.get('num2'))
            finalans = n1 + n2
            data = {
                'form':fn,
                'n1':n1,
                'n2':n2,
                'output':finalans
            }

            url = f"/student-login/?output={data['output']}"

            return HttpResponseRedirect(url)
    except Exception as e:
        print("Exception:" , e)
    return render(request,"temp_userform.html",data)

def vendorLogout(request):
    try:
        if request.session.has_key('vid'):
            del request.session['vid']
        return redirect('/vendor-login/')
    except Exception as e:
        print("Exception:",e)

def adminLogin(request):
    try:
        if request.method=="POST":
            admin_id = request.POST.get("admin_id")
            print(admin_id)
            a_password = request.POST.get("a_password")
            cursor = db.cursor()
            cursor.execute(f"select * from funding_committee where admin_id = '{admin_id}'")
            data = cursor.fetchone()
            print("hyt")
            if(a_password==data[4]):
                print(data)
                request.session['admin_id'] = admin_id
                return redirect('/admin-login/dashboard/')
    except Exception as e:
        print("Exception1:",e)
    return render(request,"adminLogin.html")

def adminDashboard(request):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            data = {
                'admin_id':admin_id,
                }
            return render(request, "adminDashboard.html", data)
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminDashboard.html")

def adminAddVendor(request):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            if request.method == "POST":
                shop_name = request.POST.get("shopname")
                location = request.POST.get("location")
                email = request.POST.get("email")
                commission = request.POST.get("commission")
                v_password = request.POST.get("v_password")
                phonenumber = request.POST.get("phonenumber")
                alternatephonenumber = request.POST.get("alternatephonenumber")
                cursor1 = db.cursor()
                cursor1.execute(f"select count(*) from vendor")
                count = cursor1.fetchone()[0]
                vid = shop_name.split()[0] + str(count+1)
                print(vid)
                cursor2 = db.cursor()
                cursor2.execute(f"insert into vendor values('{vid}', '{shop_name}', '{location}', '{email}', {commission}, {0}, '{admin_id}', '{v_password}', {0})")
                cursor3 = db.cursor()
                cursor3.execute(f"insert into vendor_mobno values('{vid}', '{phonenumber}')")
                db.commit()
                if (alternatephonenumber):
                    cursor3.execute(f"insert into vendor_mobno values('{vid}', '{alternatephonenumber}')")
                    db.commit()
            data = {
                'admin_id':admin_id,
                }
            return render(request, "adminAddVendor.html", data)
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminAddVendor.html")

def adminEditVendor(request, vid):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor1 = db.cursor()
            cursor1.execute(f"select shop_name, location, v_email, v_commission, password from vendor where vid = '{vid}' and deleted = {0}")
            details = cursor1.fetchone()
            cursor2 = db.cursor()
            cursor2.execute(f"select count(*) from vendor_mobno where vid = '{vid}'")
            count = cursor2.fetchone()[0]
            cursor3 = db.cursor()
            cursor3.execute(f"select v_mobno from vendor_mobno where vid = '{vid}'")
            phonenumbers = []
            for i in range(count):
                x = cursor3.fetchone()[0]
                phonenumbers.append(x)
            
            if len(phonenumbers) == 1:
                phonenumbers.append("-")

            if request.method == "POST":
                shop_name = request.POST.get('shopname')
                email = request.POST.get('email')
                location = request.POST.get('location')
                commission = request.POST.get('commission')
                password = request.POST.get('password')
                phonenumber = request.POST.get('phonenumber')
                alternatephonenumber = request.POST.get('alternatephonenumber')

                cursor4 = db.cursor()
                cursor4.execute(f"update vendor set shop_name = '{shop_name}', location = '{location}', v_email = '{email}', v_commission = {commission}, password = '{password}' where vid = '{vid}'")

                cursor5 = db.cursor()
                cursor5.execute(f"update vendor_mobno set v_mobno = '{phonenumber}' where vid = '{vid}'")
                if alternatephonenumber != '-':
                    cursor5.execute(f"update vendor_mobno set v_mobno = '{alternatephonenumber}' where vid = '{vid}'")
                db.commit()
                return redirect("/admin-login/dashboard/vendor-details/")
            data = {
                'admin_id':admin_id,
                'details': details,
                'phonenumbers':phonenumbers,
            }
            print("jvadh", data)

            return render(request, "adminEditVendor.html", data)
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminEditVendor.html")

def adminDeleteVendor(request, vid):
    try:
        if request.session.has_key('admin_id'):
            cursor1 = db.cursor()
            cursor1.execute(f"update vendor set deleted = 1 where vid = '{vid}'")
            db.commit()
            return redirect("/admin-login/dashboard/vendor-details/")
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminDeleteVendor.html")
    
def adminVendorDetails(request):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor1 = db.cursor()
            cursor1.execute("select vid,shop_name from vendor where deleted = 0")
            vendors = cursor1.fetchall()
            print(vendors)
            data = {
                'admin_id':admin_id,
                'vendors':vendors,
                }
            return render(request, "adminVendorDetails.html", data)
    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminVendorDetails.html")

def adminVendorViewDetails(request, vid):
    try:
        if request.session.has_key('admin_id'):
            admin_id = request.session['admin_id']
            cursor1 = db.cursor()
            cursor1.execute(f"select shop_name, location, v_email, v_commission, v_income, open from vendor where vid = '{vid}' and deleted = {0}")
            details = cursor1.fetchone()
            data = {
                'admin_id':admin_id,
                'vid':vid,
                'details':details,
                }
            return render(request, "adminVendorViewDetails.html", data)

    except Exception as e:
        print("Exception1:",e)
    return render(request, "adminVendorViewDetails.html")