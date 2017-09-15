from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.admin import StackedInline
from eventlog.models import Log
from .models import (
	Transaction,
	Milestone,
	)

admin.site.unregister(Log)


class TransactionInlineAdmin(admin.StackedInline):
	model=Transaction
	extra=1
	def get_changeform_initial_data(self, request, **kwargs):
		get_data = super(TransactionAdmin, self).get_changeform_initial_data(request)
		get_data['created_by'] = request.user.pk 
		return get_data


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):

	class Meta:
		model = Milestone

	list_display = ('id', 'title','date', 'status', 'created_by')
	list_filter_links = ('id','title', 'date')
	list_filter = ('status', 'created_by',)
	search_fields = ('feedback','title',)
	date_hierarchy = ('created')


	inlines=(TransactionInlineAdmin,)
	list_display = ('date', 'title', 'status')
	def get_changeform_initial_data(self, request, **kwargs):
		get_data = super(MilestoneAdmin, self).get_changeform_initial_data(request)
		get_data['created_by'] = request.user.pk 
		return get_data


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
	raw_id_fields = ["user"]
	list_filter = ["action", "timestamp"]
	list_display = ["timestamp", "content_type", "object_id", "user", "action", "extra"]
	search_fields = ["user__username", "user__email", "extra"]


