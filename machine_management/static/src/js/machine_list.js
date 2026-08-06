import { renderToElement } from "@web/core/utils/render";
import  publicWidget  from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
console.log("loading.......")
console.log(publicWidget)
console.log(publicWidget.registry)

var data
publicWidget.registry.machie_list= publicWidget.Widget.extend({
   selector : '.categories_section',
    willStart:async function () {
       console.log("HEllo")
       const result = await rpc('/get_top_machine_list', {})
       console.log(result)
        data=result
        const machines= result
        Object.assign(this,machines)
        console.log(machines)
    },
    start:function (){

       console.log('data.machines',data)
        const machines=this
        console.log('machines',machines)
        const chunks=chunk(data,4)
        console.log('chunks',chunks)
        chunks[0].is_active = true
        console.log('this.$target',this.$target)
        this.$target.html(renderToElement('dynamic_snippet.category_data', {chunks: chunks}))



    }

});
export function chunk(array, size) {
    const result = [];
    console.log('array',array)
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    console.log('result',result)
    return result;
}

