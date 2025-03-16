/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, useState, onMounted } from "@odoo/owl";

export class PiCustomScreen extends Component {
    setup() {
        this.state = useState({ message: "Hello from Pi Custom Screen!" });
    }

    onButtonClick() {
        alert("Nút trong form đã được click!");
    }

    showAlert() {
        alert("Bạn đã click vào nút trên Custom Screen!");
    }
}

// Đăng ký template
PiCustomScreen.template = "pi.PiCustomScreen";

// Đăng ký vào registry của Odoo
registry.category("actions").add("pi_custom_screen", PiCustomScreen);
