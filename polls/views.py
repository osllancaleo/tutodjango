#encoding:utf-8
from django.http import HttpResponse, Http404, HttpResponseRedirect
#from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from polls.models import Question, Choice
# Create your views here.

#def index(request):
#	latest_question_list = Question.objects.order_by('-pub_date')[:5]
#	template = loader.get_template('polls/index.html')
#	context = RequestContext(request, 
#		{'latest_question_list': latest_question_list,
#		})
#	return HttpResponse(template.render(context))

def index(request):
	latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'polls/index.html', context)

#def detail(request, question_id):
#	return HttpResponse("Estas viendo la pregunta %s" % question_id)

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request,'polls/detail.html',{'question': question})

def results(request,question_id):
	response = "Estas viendo los resultados de la encuesta %s"
	return HttpResponse(response % question_id)

#def vote(request,question_id):
#	return	HttpResponse("Tu vas a votar en la pregunta %s" % question_id)

def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request,'polls/detail.html',{
			'question':p,
			'error_message': "Debe elegir una de las opciones",
			})
	else:
		selected_choice.votes +=1
		selected_choice.save()
		return	HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


