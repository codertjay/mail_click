import subprocess
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View


def is_script_running():
    process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return "python3 click.py" in output.decode()


class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            is_running = is_script_running()
        except Exception as a:
            is_running = False
            print(a)
        return render(request, "index.html", {"is_running": is_running})

    def post(self, request):
        try:
            if not is_script_running():
                print("Script is not running. Re-running...")
                subprocess.Popen(['/home/ubuntu/mail_click/venv/bin/python3', '/home/ubuntu/mail_click/click.py'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as a:
            print(a)
        return redirect("home")
