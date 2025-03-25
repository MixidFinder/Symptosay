<%
import re
def render_python_code(command):
    return re.sub(r'^', '    ', command, flags=re.M)
%>revision = '${message}'
