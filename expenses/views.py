from django.db.models import Q, Sum, Count
from django.shortcuts import render
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 20

    def get_context_data(self, object_list=None, *args, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        # total_value = super(ExpenseListView, self).get_context_data(*args, **kwargs)
        # total_value['amount'] = Expense.objects.aggregate(Sum('amount'))

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            first_category = form.cleaned_data.get('first_category', '').strip()
            second_category = form.cleaned_data.get('second_category', '').strip()
            sort_by_date = form.cleaned_data.get('sort_by_date')

            if name:
                queryset = queryset.filter(name__icontains=name, )
            if start_date and end_date:
                queryset = queryset.filter(date__range=[start_date, end_date], )
            if first_category or second_category:
                queryset = queryset.filter(Q(category__name=first_category) | Q(category__name=second_category), )
            if sort_by_date == 'Ascending':
                queryset = queryset.order_by('date')
            elif sort_by_date == 'Descending':
                queryset = queryset.order_by('-date')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            **kwargs)



class CategoryListView(ListView):
    model = Category
    paginate_by = 5
    template_name = 'category_list.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(CategoryListView, self).get_context_data(*args, **kwargs)
    #     context['expense_count'] = Expense.objects.filter(category=1).annotate(Count('name'))
    #     return context
