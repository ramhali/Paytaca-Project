import { boot } from 'quasar/wrappers'
import VueQrcode from 'qrcode.vue'

export default boot(({ app }) => {
  app.component('vue-qrcode', VueQrcode)
})
