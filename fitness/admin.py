from django.contrib import admin, auth

from fitness.models import User, UserProfile, UserWeight, Food, FoodEaten, Exercise, ExercisePerformed, Muscle



class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(auth.admin.UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_goal')
    list_select_related = ('profile', )

    def get_goal(self, instance):
        return instance.profile.goal
    get_goal.short_description = 'Goal'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


class ExercisePerformedAdmin(admin.ModelAdmin):
    raw_id_fields = ("exercise",)


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(UserWeight)
admin.site.register(Food)
admin.site.register(FoodEaten)
admin.site.register(Exercise)
admin.site.register(ExercisePerformed, ExercisePerformedAdmin)
admin.site.register(Muscle)


