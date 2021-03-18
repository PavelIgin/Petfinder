from users.models.comment import Comment
import datetime


class CommentService:

    def comment_edit(self, request):
        comment_object = CommentService._get_comment_object(self)
        validated_data = CommentService._get_validated_data(self)
        if CommentService._checking_user_for_own_comment(self, comment_object, request):
            return {'status': 'You have not permissions for this comment'}
        if CommentService._check_how_old_this_comment(self, comment_object):
            return {'status': 'this comment created more then 15 minutes'}
        else:
            comment_object.comment = validated_data['edit_comment']
            comment_object.save()
            return {'status': 'comment was edited'}

    def delete_comment(self, request):
        comment_object = self._get_comment_object()
        if not self._checking_user_for_own_comment(request):
            return self._checking_user_for_own_comment(request)
        if not self._check_how_old_this_comment():
            return self._check_how_old_this_comment()
        comment_object.delete()
        return {'status': 'comment was deleted'}

    def _get_validated_data(self):
        validated_data = self.validated_data
        return validated_data

    def _get_comment_object(self):
        validated_data = CommentService._get_validated_data(self)
        return Comment.objects.get(id=validated_data['object_id'])

    def _get_time_difference(self):
        return datetime.datetime.now() - datetime.timedelta(minutes=15)

    def _checking_user_for_own_comment(self, comment_object, request):
        if request.user == comment_object.user:
            return True

    def _check_how_old_this_comment(self, comment_object):
        time_difference = CommentService._get_time_difference(self)
        comment_object = comment_object.date_create.replace(tzinfo=None)
        if comment_object > time_difference:
            return True
