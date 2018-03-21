from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # 自定义权限
    def has_object_permission(self, request, view, obj):
        # 任何人都可以看见snippets数据, 只有登入才可以删除或更新
        if request.method in permission.SAFE_METHODS:
            return True

        return obj.owner == request.user




