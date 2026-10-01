from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
import camelot
import json
import tempfile
import os



def landing_view(request):
    return render(request, "extractor/landing.html")

@login_required
def dashboard_view(request):
    return render(request, "extractor/react_index.html")
# ============================
# MAIN UI (LOGIN REQUIRED)
# ============================
@login_required
def split_view(request):
    return render(request, "extractor/split_view.html")


# ============================
# AUTH
# ============================
#def login_view(request):
#    if request.method == "POST":
#        user = authenticate(
 #           request,
  #          username=request.POST.get("username"),
   #         password=request.POST.get("password")
  #      )
   #     if user:
   #         login(request, user)
    #        return redirect("/")
    #    return render(request, "registration/login.html", {
    #        "error": "Invalid username or password"
    #    })

   # return render(request, "registration/login.html")



@login_required
def logout_view(request):
    logout(request)
    return redirect("/login/")


# ============================
# UPLOAD PDF & EXTRACT TABLES
# (NO login_required — VERY IMPORTANT)
# ============================
@csrf_exempt
def upload_and_extract(request):
    if request.method != "POST":
        return JsonResponse({"success": False})

    pdf_file = request.FILES.get("pdf")
    if not pdf_file:
        return JsonResponse({"success": False})

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        for chunk in pdf_file.chunks():
            tmp.write(chunk)
        pdf_path = tmp.name

    tables = []

    try:
        extracted = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")

        for table in extracted:
            df = table.df
            headers = df.iloc[0].tolist()
            rows = []

            for i in range(1, len(df)):
                row = {}
                for j, h in enumerate(headers):
                    row[h.strip()] = df.iloc[i, j].strip()
                rows.append(row)

            tables.append({
                "headers": headers,
                "rows": rows
            })

    finally:
        os.remove(pdf_path)

    request.session["tables"] = tables
    request.session.modified = True

    return JsonResponse({"success": True})


# ============================
# ANALYZE HIGHLIGHTED TEXT
# ============================
@csrf_exempt
def analyze_selection(request):
    body = json.loads(request.body)
    keyword = body.get("keyword", "").lower()

    tables = request.session.get("tables", [])
    matched_rows = []

    for table in tables:
        key_col = table["headers"][0]
        for row in table["rows"]:
            if keyword in row.get(key_col, "").lower():
                matched_rows.append(row)

    return JsonResponse({"rows": matched_rows})


# ============================
# QUERY ENTIRE TABLE
# ============================
@csrf_exempt
def query_table(request):
    body = json.loads(request.body)
    query = body.get("query", "").lower()

    tables = request.session.get("tables", [])
    results = {}

    for table in tables:
        for header in table["headers"]:
            if any(word in header.lower() for word in query.split()):
                total = 0
                for row in table["rows"]:
                    val = row.get(header, "")
                    try:
                        total += float(
                            "".join(c for c in val if c.isdigit() or c == ".")
                        )
                    except:
                        pass
                results[header] = total

    return JsonResponse({"results": results})
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "registration/register.html", {
                "error": "Username already exists"
            })

        # ✅ Django hashes password automatically
        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("/login/")

    return render(request, "registration/register.html")