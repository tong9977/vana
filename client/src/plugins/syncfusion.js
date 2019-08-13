import Vue from 'vue'
import { GridPlugin } from '@syncfusion/ej2-vue-grids';
import { CalendarPlugin } from '@syncfusion/ej2-vue-calendars';
import { DatePickerPlugin } from '@syncfusion/ej2-vue-calendars';
import { DateTimePickerPlugin } from '@syncfusion/ej2-vue-calendars';
//*import { SchedulePlugin, Day, Week, WorkWeek, Month, Agenda, View, Resize, DragAndDrop } from "@syncfusion/ej2-vue-schedule";


/*Vue.use(SchedulePlugin); */
Vue.use(DateTimePickerPlugin);
Vue.use(DatePickerPlugin);
Vue.use(GridPlugin);
Vue.use(CalendarPlugin);