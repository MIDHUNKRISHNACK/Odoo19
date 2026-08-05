import { renderToElement } from "@web/core/utils/render";
import  publicWidget  from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
console.log("loading.......")
console.log(publicWidget)
console.log(publicWidget.registry)
publicWidget.registry.machie_list= publicWidget.Widget.extend({
   selector : '.categories_section',
    willStart:async function () {
       console.log("HEllo")
       const result = await rpc('/get_top_machine_list', {})
       console.log(result)
        if(result){
           this.$target.html(renderToElement('dynamic_snippet.category_data', {result: result}))
       }

   },

});

