from django.shortcuts import render , redirect
from .models import Student , Group , School , Sport
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from .utils import generate_pdf
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.http import FileResponse, Http404


# Create your views here.

def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(id_number__icontains=query) |
            Q(school__name__icontains=query) |
            Q(group__name__icontains=query)
        )

    return render(request, 'myapp/student_list.html', {
        'students': students,
        'query': query
    })
    
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    schools = School.objects.all()
    groups = Group.objects.all()

    if request.method == 'POST':
        student.name = request.POST['name']
        student.id_number = request.POST['id_number']
        student.father_name = request.POST['father_name']
        student.gender = request.POST['gender']
        student.dob = request.POST['dob']
        student.sports = request.POST['sports']
        student.school_id = request.POST['school']
        student.group_id = request.POST['group']
        
        if 'image' in request.FILES:
            student.image = request.FILES['image']

        student.save()
        return redirect('student_list')

    return render(request, 'myapp/edit_student.html', {
        'student': student,
        'schools': schools,
        'groups': groups
    })
    
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('student_list')

    return render(request, 'myapp/delete_confirm.html', {'student': student})


def register(request):
    groups = Group.objects.all()
    schools = School.objects.all()

    # ✅ Load session data if returning from confirmation edit
    form_data = request.session.get('form_data')
    selected_sports = form_data['sports'].split(', ') if form_data and 'sports' in form_data else []

    if request.method == 'POST':
        name = request.POST['name']
        id_number = request.POST['id_number']
        father_name = request.POST['father_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        school_id = request.POST['school']
        group_id = request.POST['group']
        image = request.FILES.get('image')  # None if editing without changing file

        # ✅ Get selected sports from form (checkbox list)
        selected_sports = request.POST.getlist('sports')

        # ❌ Validate: exactly 2 sports must be selected
        if len(selected_sports) != 2:
            return HttpResponse("❌ Error: Please select exactly 2 sports.")

        # ❌ Check for duplicate ID (only if not editing)
        if not form_data and Student.objects.filter(id_number=id_number).exists():
            return HttpResponse("❌ Error: This ID number is already registered.")

        # ✅ Prepare sports string
        sports_string = ", ".join(selected_sports)

        # ✅ Create new student record
        Student.objects.create(
            name=name,
            id_number=id_number,
            father_name=father_name,
            dob=dob,
            gender=gender,
            image=image,
            sports=sports_string,
            school_id=school_id,
            group_id=group_id
        )

        # ✅ Clear session after successful registration
        request.session.pop('form_data', None)

        return HttpResponse("✅ Registration Successful!")

    # 🟡 Render form (GET) with prefilled data if exists
    return render(request, 'myapp/register.html', {
        'groups': groups,
        'schools': schools,
        'form_data': form_data,
        'selected_sports': selected_sports,
    })

def get_sports_by_group(request):
    group_id = request.GET.get('group_id')
    sports = Sport.objects.filter(group_id=group_id).values('id', 'name')
    return JsonResponse(list(sports), safe=False)

def confirm(request):
    if request.method == "POST":
        name = request.POST['name']
        id_number = request.POST['id_number']
        father_name = request.POST['father_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        school_id = request.POST['school']
        group_id = request.POST['group']
        sports_list = request.POST.getlist('sports')

        # ✅ 1. Validate exactly 2 sports selected
        if len(sports_list) != 2:
            return HttpResponse("❌ Error: Please select exactly 2 sports.")

        # ✅ 2. Check for duplicate registration (only if not editing)
        if 'form_data' not in request.session and Student.objects.filter(id_number=id_number).exists():
            return HttpResponse("❌ Error: This ID number is already registered.")

        # ✅ 3. Handle image
        image = request.FILES.get('image')
        image_path = None
        image_url = None

        if image:
            # Save uploaded image to media/temp/
            fs = FileSystemStorage(location='media/temp/')
            filename = fs.save(image.name, image)
            image_path = filename
            image_url = f"/media/temp/{filename}"
        else:
            # Use previously uploaded image from session if available
            image_path = request.session.get('form_data', {}).get('image_path')
            image_url = f"/media/temp/{image_path}" if image_path else None

        # ✅ 4. Save form data in session
        request.session['form_data'] = {
            'name': name,
            'id_number': id_number,
            'father_name': father_name,
            'dob': dob,
            'gender': gender,
            'school': school_id,
            'group': group_id,
            'sports': ', '.join(sports_list),
            'image_path': image_path,
        }

        # ✅ 5. Get school/group names from DB
        school_name = School.objects.get(id=school_id).name
        group_name = Group.objects.get(id=group_id).name

        # ✅ 6. Show confirmation page
        return render(request, 'myapp/confirm.html', {
            'name': name,
            'id_number': id_number,
            'father_name': father_name,
            'dob': dob,
            'gender': gender,
            'school_name': school_name,
            'group_name': group_name,
            'sports': ', '.join(sports_list),
            'image_url': image_url
        })

    else:
        return redirect('/')
    

    
    
def submit(request):
    if request.method == "POST":
        data = request.session.get('form_data')
        if not data:
            return redirect('registerpage')

        filename = os.path.basename(data['image_path'])
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)
        final_path = os.path.join(settings.MEDIA_ROOT, 'students', filename)

        # Move image from temp to permanent
        if os.path.exists(temp_path):
            if os.path.exists(final_path):
                os.remove(final_path)
            os.rename(temp_path, final_path)
        else:
            return HttpResponse("❌ Image file not found. Please re-upload.")

        # ✅ Convert sports list to comma-separated string
        if isinstance(data['sports'], list):
            data['sports'] = ', '.join(data['sports'])

        # Save student
        student = Student.objects.create(
            name=data['name'],
            id_number=data['id_number'],
            father_name=data['father_name'],
            dob=data['dob'],
            gender=data['gender'],
            school_id=data['school'],
            group_id=data['group'],
            sports=data['sports'],
            image='students/' + filename
        )

        # Generate PDF bytes
        pdf_bytes = generate_pdf(student, request)

        # Save PDF to media/pdfs/
        output_dir = os.path.join(settings.MEDIA_ROOT, 'pdfs')
        os.makedirs(output_dir, exist_ok=True)

        pdf_filename = f"{student.id}_registration.pdf"
        pdf_full_path = os.path.join(output_dir, pdf_filename)

        with open(pdf_full_path, 'wb') as f:
            f.write(pdf_bytes)

        # Prepare PDF path for template
        pdf_path = os.path.join(settings.MEDIA_URL, 'pdfs', pdf_filename)

        # Clear session
        del request.session['form_data']

        # Split sports string for display
        sports_list = [s.strip() for s in student.sports.split(',')] if student.sports else []

        return render(request, 'myapp/thankyou.html', {
            'student': student,
            'pdf_path': pdf_path,
            'sports_list': sports_list
        })

    return redirect('registerpage')

def download_pdf(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    pdf_file = generate_pdf(student, request)

    custom_filename = f"Sports_Registration_{student.id_number}.pdf"
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{custom_filename}"'  # Or use attachment for download

    return response

