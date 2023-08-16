from django.views.generic.edit import CreateView
from orders.forms import OrderForms
from django.urls import reverse_lazy


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForms
    success_url = reverse_lazy('orders:order_create')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
