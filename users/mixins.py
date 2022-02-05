from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin

class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

# LoggedOutOnlyView를 뷰 안에 놓을 때마다 test_func을 부르고 이 값은 true를 반환해야하고
# true는 유저의 인증이 되지 않았다는 것을 의미한다 (즉 익명의 유저)

    def handle_no_permission(self):
        return redirect("core:home")