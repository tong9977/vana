

<template>
  <q-page padding>

   <q-card class="my-card ">
    <div class="row q-col-gutter-sm" style="margin-left:20px;">
      
        <div class="col-12 col-md-3">
          <q-input filled v-model="date" mask="date" :rules="['date']">
            <template v-slot:append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                  <q-date
                    v-model="date"
                    :format="dateFormat"
                    @input="() => $refs.qDateProxy.hide()"
                  />
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>
        </div>
        <div class="col-12 col-md-3">
          <q-select v-model="stationselect" :options="station" label="Station" />
        </div>

        <div class="col-12 col-md-3">
          <q-select v-model="sizeselect" :options="size" label="Size" />
        </div>
        <div class="col-12 col-md-3">
          <q-btn color="primary" style="margin-top:15px;" icon="search" @click="OK()" />
        </div>
     
    </div>
     </q-card>
    <br />

    <p class="text-subtitle1 text-weight-bolder">Total {{total}} picture</p>
    <div class="q-col-gutter-md row items-start">
      <div class="col-6 col-md-4" v-for="item in items" :key="item">
        <q-img :src="item.Url" style="width: 100%">
          <div class="absolute-bottom  ">
            <span class="text-subtitle1 text-left"><q-icon name="access_time" />  {{item.TakenTime |fulldatetime}} </span> <span class="q-pl-md text-subtitle1 ">{{item.RFIDString}}</span>
          </div>
        </q-img>
      </div>
    </div>
  </q-page>
</template>

<script>
import { mapState } from "vuex";
import { createDateFilter } from "vue-date-fns";
import locale from "date-fns/locale/th";

import { startOfDay, endOfDay, format, addHours } from "date-fns";
export default {
  data: () => ({
    //--start config
    service: "photo",
    objectName: "Photo",

    query: { $sort: { Id: -1 } },
    //--end config
    total: 0,
    stationselect: "",
    station: ["rattler", "innertube"],
    size: ["s", "m", "l"],
    sizeselect: "",
    items: [],
    date: new Date(),
    dateFormat: "dd-MM-yyyy"
  }),
  computed: {},
  async mounted() {
    //init here

  },
  filters: {
    date: createDateFilter("DD/MM/YY", { locale }),
    dateC: createDateFilter("HH:mm", { locale }),
    fulldatetime: createDateFilter("DD/MM/YYYY HH:mm:ss", { locale })
  },
  methods: {
    async OK() {
      try {
        const q = {};
        var sDate = startOfDay(new Date(this.date));
        var eDate = endOfDay(new Date(this.date));

        var x = format(addHours(sDate, -7), "YYYY-MM-DDTHH:mm:ss");
        var y = format(addHours(eDate, -7), "YYYY-MM-DDTHH:mm:ss");

        q.TakenTime = {
          $gt: x,
          $lt: y
        };

        q.Station = this.stationselect;
        q.Size = this.sizeselect;

        var res = await this.$store.dispatch("photo/find", { query: q });
        this.total = res.total;
        this.items = res.data;
      } catch (error) {
        console.log(error);
        alert("ไม่สามารถขอข้อมูลจาก server ได้" + error);
      }
    }
  }
};
</script>
<style>
.my-card {
 
  width: 100%;
}
</style>