#encoding:utf-8
from django.http import HttpResponse, Http404, HttpResponseRedirect
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic #Para terceras vistas.
from polls.models import Question, Choice


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		#Retorna las últimas 5 preguntas publicadas
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	template_name = 'polls/detail.html'
	model= Question

class ResultsView(generic.DetailView):
	template_name = 'polls/results.html'
	model = Question	

def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		#Busca si se seleccionó alguna opción y se autoenvió el formulario.
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#Entra por default en en este render
		return render(request,'polls/detail.html',{
			'question':p,
			'error_message': "Debe elegir una de las opciones...",
			})
	else:
		#Si se seleccionó algo, ingresa a esta opción
		selected_choice.votes +=1
		selected_choice.save()
		return	HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
