<template>
  <q-layout view="hHh LpR fFf" class="bg-grey-3">
    <q-header class="bg-grey-3 text-grey-9" reveal>
      <q-toolbar class="GPLAY__toolbar text-grey-6">
        <q-btn
          v-if="this.$q.platform.is.mobile || !leftDrawerOpen"
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
          icon="menu"
          class="q-mr-sm"
        />

        <div class="q-pr-lg" v-if="$q.screen.gt.xs">
          <img
            class="GPLAY__logo"
            src="assets/img/vananavalogo.png"
          />
        </div>

        <q-space />

        <div class="GPLAY__toolbar-input-container row no-wrap">
          
        </div>

        <q-space />

        <div class="q-pl-md q-gutter-sm row no-wrap items-center">
          <q-btn round dense flat color="grey-8" size="14px" icon="apps"></q-btn>

          <q-btn round dense flat color="grey-8" icon="notifications">
            <q-badge color="red" text-color="white" floating>2</q-badge>
          </q-btn>

          <q-btn round flat>
            <q-avatar size="26px">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
            </q-avatar>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" bordered content-class="bg-grey-3 text-grey-7" :width="200">
      <q-list>
        

        <q-item clickable class="GPLAY__drawer-link GPLAY__drawer-link--apps">
          <q-item-section avatar class="bg-green-7 text-grey-1 text-center">
            <q-icon name="search" />
          </q-item-section>
          <q-item-section class="apps-text">
            <q-item-label>Search</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable class="GPLAY__drawer-link GPLAY__drawer-link--movies">
          <q-item-section avatar class="movies-icon bg-red-7 text-grey-1 text-center">
            <q-icon name="camera_alt" />
          </q-item-section>
          <q-item-section class="movies-text">
            <q-item-label>Test Camera</q-item-label>
          </q-item-section>
        </q-item>


        <q-separator class="q-mb-md" />

        
      </q-list>
    </q-drawer>

    <q-page-container>
      
      <q-page-sticky expand position="top" >
        <q-toolbar class="GPLAY__sticky bg-white q-px-xl">
          <q-space />
          
        </q-toolbar>
      </q-page-sticky>
      <router-view />

    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "GooglePlayLayout",
  data() {
    return {
      leftDrawerOpen: this.$q.screen.width >= 992,
      search: "",
      storage: 0.26,
      
    };
  }
};
</script>

<style lang="stylus">
.GPLAY {
  &__toolbar {
    height: 60px;
  }

  &__logo {
    width: 183px;
    height: 39px;
  }

  &__toolbar-input-container {
    min-width: 100px;
    width: 80%;
  }

  &__toolbar-input-btn {
    border-radius: 0;
    max-width: 60px;
    width: 100%;
  }

  &__drawer-link {
    .q-item__section--avatar {
      margin: -8px 0 -8px -16px;
      padding: 8px 0 8px 16px;
    }

    .q-item__section--main {
      margin: -8px -16px -8px 16px;
      padding: 8px 16px 8px 2px;
      font-size: 18px;
      font-weight: 300;
    }

    &--apps, &--movies, &--music, &--books, &--devices {
      background: #f5f5f5 !important;

      &:hover {
        color: #eee !important;
      }
    }

    &--apps:hover {
      background: #43a047 !important;
    }

    &--movies:hover {
      background: #e53935 !important;
    }

    &--music:hover {
      background: #fb8c00 !important;
    }

    &--books:hover {
      background: #1e88e5 !important;
    }

    &--devices:hover {
      background: #546e7a !important;
    }
  }

  &__drawer-item {
    padding: 6px 12px 6px 23px;
  }

  &__sticky {
    min-height: 49px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  }

  &__sticky-help {
    border: 1px solid #ccc;
    padding-left: 8px;
    padding-right: 8px;
  }

  &__sticky-settings {
    padding-left: 17px;
    padding-right: 17px;
    border: 1px solid #ccc;
  }
}
</style>