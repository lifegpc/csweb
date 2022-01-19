/**
 * @class Generate a key and value input list
 */
class InputList {
    /**
     * Initialize Input List
     * @param {Element} base The Element to render the list
     * @param {(modified: {k: string, v: string} | undefined, data: Object<string, {k: string, v: string}>)=>void | undefined} update The callback function when data was updated
     * @param {number | undefined} minWidth The min size of key inputbox.
     */
    constructor(base, update, minWidth) {
        /**@type {Element} The Element to render the list*/
        this.base = base;
        /**@type {Object<string, {k: string, v: string}>} The location to store data*/
        this._data = {};
        /**@type {(modified: {k: string, v: string} | undefined, data: Object<string, {k: string, v: string}>)=>void | undefined} The callback function when data was updated*/
        this.update = update;
        /**@type {Number} The newest input list ID*/
        this.id = 0;
        /**@type {Number} The count of the input list*/
        this.count = 0;
        /**@type {Object<string, HTMLInputElement>}*/
        this.minusb = {};
        /**@type {Number} The min size of key inputbox.*/
        this.minWidth = minWidth ? minWidth : 50;
        this.add()
    }
    /**
     * Add a new pair to specified location
     * @param {Number | undefined} index The location want to insert. If not specified, insert to the last.
     */
    add(index) {
        let div = document.createElement('div');
        div.setAttribute('i', this.id);
        let data = { k: "", v: "" };
        this._data[this.id] = data;
        let inp1 = document.createElement('input');
        inp1.style.width = "20%";
        inp1.style.minWidth = this.minWidth + "px";
        inp1.addEventListener('input', () => {
            data.k = inp1.value;
            if (this.update) this.update(data, this._data);
        })
        div.append(inp1);
        div.append(" = ");
        let inp2 = document.createElement('input');
        inp2.style.width = "60%";
        inp2.style.minWidth = (this.minWidth * 3) + "px";
        inp2.addEventListener('input', () => {
            data.v = inp2.value;
            if (this.update) this.update(data, this._data);
        })
        div.append(inp2);
        let minus = document.createElement('input');
        minus.type = "button";
        minus.value = "-";
        this.minusb[this.id] = minus;
        minus.addEventListener('click', () => {
            this.removeDiv(div);
        })
        div.append(minus);
        let add = document.createElement('input');
        add.type = "button";
        add.value = "+";
        ((inputi) => {
            add.addEventListener('click', () => {
                this.add(inputi);
            })
        })(this.id);
        div.append(add);
        /**@type {Element}*/
        let child = null;
        if (index != undefined) {
            for (let i = 0; i < this.base.childElementCount; i++) {
                child = this.base.children[i];
                if (parseInt(child.getAttribute("i")) == index) {
                    child = child.nextElementSibling
                }
            }
        }
        child ? this.base.insertBefore(div, child) : this.base.append(div);
        this.id++;
        this.count++;
        this.checkButtonStatus();
        if (this.update) this.update(data, this._data);
    }
    checkButtonStatus() {
        let l = Object.getOwnPropertyNames(this.minusb);
        let c = l.length;
        l.forEach((key) => {
            this.minusb[key].disabled = c < 2;
        })
    }
    data() {
        return this._data;
    }
    destory() {
        for (let i = 0; i < this.base.childElementCount; i++) {
            this.removeDiv(this.base.children[i]);
        }
    }
    isEmpty() {
        let l = Object.getOwnPropertyNames(this._data);
        for (let i = 0; i < l.length; i++) {
            let d = this._data[l[i]];
            if (d.k.length || d.v.length) return false;
        }
        return true;
    }
    /**
     * Remove Input div
     * @param {HTMLInputElement} div Target element
     */
    removeDiv(div) {
        let ind = parseInt(div.getAttribute("i"));
        div.parentElement.removeChild(div);
        delete this.minusb[ind];
        delete this._data[ind];
        this.count--;
        this.checkButtonStatus();
        if (this.update) this.update(undefined, this._data);
    }
    /**
     * @returns {Object<string, string>}
     */
    toObject() {
        let o = {};
        Object.getOwnPropertyNames(this._data).forEach((key) => {
            let d = this._data[key];
            o[d.k] = d.v;
        })
        return o;
    }
}

module.exports = { InputList }
