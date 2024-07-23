// TODO: Search for relative xpath instead
function getElementXpath(element) {
    let paths = [];
    for (; element && element.nodeType == 1; element = element.parentNode) {
        let index = 0;
        for (let sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {
            if (sibling.nodeType == Node.DOCUMENT_TYPE_NODE)
                continue;
            if (sibling.nodeName == element.nodeName)
                ++index;
        }
        let tagName = element.nodeName.toLowerCase();
        let pathIndex = (index ? "[" + (index + 1) + "]" : "");
        paths.splice(0, 0, tagName + pathIndex);
    }
    return paths.length ? "/" + paths.join("/") : null;
}

function logElementAction(event, actionType) {
    console.log(event)
    let element = event.target

    // Generate attribute object
    let attributes = {}
    for (let attr of element.attributes) {
        attributes[attr.name] = attr.value
    }

    // Generate element info object
    let elementInfo = {
        tagName: element.tagName,
        attributes: attributes,
        xpath: getElementXpath(element),
        outerHTML: element.outerHTML
    }

    // Key is only present in certain events like keydown
    if (event.key) {
        key = event.key
    }
    else {
        key = 'mouse'
    }

    let actionInfo = {
        action: actionType,
        key: key,
        element: elementInfo
    }

    if (!window.loggedElementInfo) {
        window.loggedElementInfo = []
    }

    window.loggedElementInfo.push(JSON.stringify(actionInfo))
}

document.addEventListener('click', function(event) {
    logElementAction(event, 'click')
}, true)

document.addEventListener('contextmenu', function(event) {
    logElementAction(event, 'contextmenu')
}, true)

document.addEventListener('dblclick', function(event) {
    logElementAction(event, 'dblclick')
}, true)

document.addEventListener('keydown', (event) => {
    logElementAction(event, 'keydown')
}, true)