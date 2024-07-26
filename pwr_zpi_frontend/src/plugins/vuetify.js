import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import '@fortawesome/fontawesome-free/css/all.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            dark: {
                primary: '#5c0a0a',
                secondary: colors.blueGrey.darken1,
                accent: '#8e3a31',
                error: '#ff5252',
                info: '#3c1966',
                success: '#1c3d0f',
                warning: '#828217',
                'primary-text': '#ff8862',
                anchor: '#dea6a0',
            },
        },
        dark: true,
        options: { customProperties: true }
    }
});
