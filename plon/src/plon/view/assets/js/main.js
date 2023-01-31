
function js_print(...msg) {
    let console = document.getElementById("console_view")
    console.innerHTML += "<div class='message'>"+msg+"</div>";
}

var sessionOutput = function(session, string){
    let console = document.getElementById("console_view")
    let div = document.createElement('div')
    let inputField = document.getElementById('input_field')
    div.className = 'console'

    // clone
    // strip ids

    let span = document.createElement('span')
    span.innerText = string
    span.className = 'text'

    div.appendChild(span)
    console.appendChild(div)

    //console.innerHTML += "<div class='console'><span class='text'>"+string+"</span></div>";

    // move the input field to the new console line.
    let items = document.getElementsByClassName('console')
    let item = items.item(items.length-1)
    item.appendChild(inputField)
    window.scrollTo(0,document.body.scrollHeight);
}

window.onload = function(){
    js_print("Javascript", "window.onload", "Called");
    js_print("Javascript", "python_property", python_property);
    wake_ready({ name: 'main'})
    //js_print("Javascript", "navigator.userAgent", navigator.userAgent);
    //js_print("Javascript", "cefpython_version", cefpython_version.version);
    //html_to_data_uri("test", js_callback_1);
    //external.test_multiple_callbacks(js_callback_2);
}

function placeCaretAtEnd(el) {
    el.focus();
    if (typeof window.getSelection != "undefined"
            && typeof document.createRange != "undefined") {
        var range = document.createRange();
        range.selectNodeContents(el);
        range.collapse(false);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    } else if (typeof document.body.createTextRange != "undefined") {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(el);
        textRange.collapse(false);
        textRange.select();
    }
}

document.onkeydown = function(evt) {
    let ev = evt || window.event;
    let fieldText = document.getElementById('input_field_text')

    let text = ev.key
    if (ev.ctrlKey) {
        text = '\x1B'
    }

    if(ev.keyCode == 13) {
        // enter
        fieldText.innerText = ''
        text = "\r\n"
    }

    if(ev.keyCode == 9) {
        // tab
        fieldText.innerText = ''
        text = "\t"
    }
    console.log(ev.keyCode, ev.key)

    sessionKeyInput('main', {code: ev.keyCode, key: ev.key})
    //sessionInput('main', text)

    //fieldText.innerText = ''
    if(document.activeElement != fieldText) {
        fieldText.focus()
        if(fieldText.innerText.length > 0) {
            placeCaretAtEnd(fieldText);
        }
    }
    if(ev.keyCode == 13) {
        return false
    }

    //terminalType(ev.key)
};
