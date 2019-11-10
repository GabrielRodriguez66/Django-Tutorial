import io

from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
            Excludes any questions that aren't published yet.
        """
        return [q for q in Question.objects.published_recently(5) if q.has_choices()]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def delete_question(request, question_id):
    get_object_or_404(Question, pk=question_id).delete()
    return HttpResponseRedirect(reverse('polls:index'))


def edit(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.question_text = request.POST["new_text"]
    question.save()
    count = 1
    for ch in question.choice_set.all():
        new_choice_text = request.POST["choice"+str(count)]
        if new_choice_text:
            ch.choice_text, ch.votes = new_choice_text, 0
            ch.save()
        else:
            ch.delete()
        count += 1
    return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))


def add_question(request):
    if request.POST["choice1"]:
        question = Question(question_text=request.POST["question_text"], pub_date=timezone.now())
        question.save()
        Choice.objects.create(question=question, choice_text=request.POST["choice1"], votes=0)
        if request.POST["choice2"]:
            Choice.objects.create(question=question, choice_text=request.POST["choice2"], votes=0)
        if request.POST["choice3"]:
            Choice.objects.create(question=question, choice_text=request.POST["choice3"], votes=0)
    return HttpResponseRedirect(reverse('polls:index'))


def home(request):
    return render(request, 'polls/base.html')


class ExportPDFView(generic.View):

    @staticmethod
    def table(pdf, x, y, question):

        # Table headers
        headers = ('Choice Text', 'Votes')

        # Questions tuples
        details = [(ch.choice_text, ch.votes) for ch in question.choice_set.all()]

        # Establecemos el tamaño de cada una de las columnas de la tabla
        table = Table([headers] + details, colWidths=[4 * cm, 4 * cm])

        # Aplicamos estilos a las celdas de la tabla
        table.setStyle(TableStyle(
            [
                # La primera fila(headers) va a estar centrada
                ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))

        # Establecemos el tamaño de la hoja que ocupará la tabla
        table.wrapOn(pdf, 800, 600)

        # Definimos la coordenada donde se dibujará la tabla
        table.drawOn(pdf, x, y)

    @staticmethod
    def get(request):
        # Indicate content type, in this case pdf
        response = HttpResponse(content_type='application/pdf')

        # temp storage
        buffer = io.BytesIO()

        # Canvas allow us to use coordinates
        pdf = canvas.Canvas(buffer)

        # Header
        pdf.setFont("Helvetica", 24)
        pdf.drawString(250, 790, "Questions")

        pdf.setFont("Helvetica", 12)
        questions = IndexView().get_queryset()
        x, y, count = 55, 745, 1

        for q in questions:
            if count != 1:
                y -= 45
            pdf.drawString(x, y, str(count) + ". " + q.question_text)
            count += 1
            y -= 45

            ExportPDFView.table(pdf, x+30, y - 19, q)

        pdf.showPage()  # cut the page in order to go to the next one
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)  # add pdf to the response

        return response

