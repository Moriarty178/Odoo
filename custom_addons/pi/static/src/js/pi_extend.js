 import { registry } from "@web/core/registry";
 import { useService } from "@web/core/utils/hooks";
 import { Component, useState, onMounted } from "@odoo/owl";

 export class PiExtend extends Component {
    setup() {
        // this.state = useState({ message: "WWWHHHAAATTT?"});
        this.notification = useService("notification");
    }
    onClick() {
//        this.notification.add({type: 'success', message: 'Success!'});
        this.notification.add("Hello from Odoo 17!", { type: "info" });
    }
}

// sub template
PiExtend.template = "pi.PiExtend";

// sub registry 
registry.category("fields").add("pi_extend", {
    Component: PiExtend,
    viewType: "form",
    model: "pi.pi_model"
});

