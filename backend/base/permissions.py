from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin

def entrepreneur_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.has_perm('crowdfunding.is_entrepreneur'),
        login_url='/login/',
        redirect_field_name=None
    )
    return actual_decorator(view_func)

def investor_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.has_perm('crowdfunding.is_investor'),
        login_url='/login/',
        redirect_field_name=None
    )
    return actual_decorator(view_func)

def admin_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.has_perm('crowdfunding.is_admin'),
        login_url='/login/',
        redirect_field_name=None
    )
    return actual_decorator(view_func)

class EntrepreneurRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('crowdfunding.is_entrepreneur')
    
    def handle_no_permission(self):
        raise PermissionDenied("You don't have permission to access this page.")

class InvestorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('crowdfunding.is_investor')
    
    def handle_no_permission(self):
        raise PermissionDenied("You don't have permission to access this page.")

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('crowdfunding.is_admin')
    
    def handle_no_permission(self):
        raise PermissionDenied("You don't have permission to access this page.")