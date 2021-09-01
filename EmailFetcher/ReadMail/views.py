from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
# Create your views here.
import imaplib
import email

def index(request):
    if request.user.is_anonymous:
        return HttpResponse("404 page not found")
    if request.method == 'POST':
        ispname = request.POST.get('ispName','')
        emailid = request.POST.get('email','')
        password = request.POST.get('password','')
        folderName = request.POST.get('folderName','')
        countOfMail = request.POST.get('countOfMail', '')
        field = request.POST.get('field','')
        if not countOfMail:
            countOfMail = "0"
        print(field)
        print(type(field))
        #mylist = list(field.split())
        #print(mylist)

        if "Hotmail" in ispname:
            resukt = hotmailMailFetch(emailid, password, folderName, countOfMail, field)
            return render(request, 'ReadMail/index.html', resukt)
    return render(request,'ReadMail/index.html')



def hotmailMailFetch(emailid,emailpassword,foldername,countofmail,field):
    username = emailid
    password = emailpassword


    mail = imaplib.IMAP4_SSL('outlook.office365.com')
    try:
        status, summary = mail.login(username, password)
        if status == "OK":
            print(summary)
    except mail.error:
        context = {'error': 'error_msg', 'errorMessage': 'Authentication failed: Please check your emailid or password'}
        return context

    result, mailboxes = mail.list()
    if result == "OK":
        print(mailboxes)
    else:
        context = {'error': 'error_msg', 'errorMessage': 'Error retreiving mailbox information'}
        return context

    alldata = []
    mail.select(foldername)
    result, numbers = mail.uid('Search', None, 'ALL')
    uids = numbers[0].decode().split()
    countofmail = int(countofmail) * (-1)
    result, messages = mail.uid('fetch', ','.join(uids[countofmail:]), '(BODY.PEEK[HEADER])')
    i = 1
    for _, message in messages[::2]:
        msg = email.message_from_bytes(message)
        # print('{}'.format(msg.get('subject')))
        alldata.append(i)
        alldata.append(msg.get(field))
        i = i + 1
    # alldata.append(dict(msg))
    res_dct = {alldata[i]: alldata[i + 1] for i in range(0, len(alldata), 2)}  # to convert list into dictionary
    context = {"data": res_dct, 'foldername': foldername, 'fieldname':field}
    #print(res_dct)
    # except Exception as ex:
    # return render(request,'index.html', {'error': 'error_msg'})
    return context

def handleLogout(request):
    logout(request)
    return redirect('index')


