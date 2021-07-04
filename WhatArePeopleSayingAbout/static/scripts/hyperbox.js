// Our custom built front end JS framework to handle dynamic content in JS!
const Hpx = (() => {
    const extractEventName = (name) => {
        return name.slice(2).toLowerCase();
    }
    
    const isEventProp = (name) => {
        return /^on/.test(name);
    }
    
    const isCustomProp = (name) => {
        return isEventProp(name) || name === 'forceUpdate';
    }    
    
    const addEventListeners = (target, props = {}) => {
        Object.keys(props).forEach(name => {
            if (isEventProp(name)) {
              target.addEventListener(
                extractEventName(name),
                props[name]
              );
            }
        });
    }
    
    const setBoolProp = (target, name, value) => {
        if (value) {
            target.setAttribute(name, value);
            target[name] = true;
        } else {
            target[name] = false;
        }
    }
    
    const setStyleProps = (target, props) => {
        Object.keys(props).forEach(propKey => {
            target.style[propKey] = props[propKey];
        });
    }
    
    const setProp = (target, name, value) => {
        if (isCustomProp(name)) return;
        if (name === 'className') {
            target.setAttribute('class', value);
        } else if (name === 'style' && typeof value === 'object') {
            setStyleProps(target, value);
        } else if (typeof value === 'boolean') {
            setBoolProp(target, name, value);
        } else {
            target.setAttribute(name, value);
        }
    }
    
    const setProps = (target, props) => {
        if (!props) return;
        Object.keys(props).forEach(prop => {
            setProp(target, prop, props[prop]);
        });
    }

    return {
        setProps,
        addEventListeners
    }
})()

const x = (type, props, ...children) => {
    return { type, props: props || {}, children }
}

const createElement = (xNode) => {
    if (!xNode) return null;
    const { type, props, children } = xNode;
    if (typeof xNode !== 'object') return document.createTextNode('' + xNode);
    const el = document.createElement(type);
    Hpx.setProps(el, props);
    Hpx.addEventListeners(el, props);
    // If oninit listener included, call it!
    if (typeof xNode.props.oninit === 'function') xNode.props.oninit(el);
    if (children) children
        .map(createElement)
        .forEach(child => {
            if (child) el.appendChild(child)
        });
    return el;
}