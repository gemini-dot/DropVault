# User Database Schema (DropVault)
**Version:** 1.0.0
**Author:** CuSam

## 1. Overview
Cấu trúc JSON lưu trữ thông tin người dùng trong MongoDB.

## 2. JSON Structure
​```json
{
  "auth": {
    "gmail": "lai-van-sam@gmail.com",
    "password": "$argon2id$v=19$m=65536,t=3,p=4$...",
    "role": "user",
    "status": "active"
  },
  "profile": {
    "display_name": "CuSam",
    "avatar_url": "/static/img/default-avatar.png",
    "created_at": "2026-04-18T19:56:00Z",
    "updated_at": "2026-04-18T19:56:00Z"
  },
  "storage": {
    "root_folder_id": "unique_folder_uuid",
    "total_space_bytes": 10737418240,
    "used_space_bytes": 0,
    "plan": "free"
  },
  "settings": {
    "theme": "dark",
    "language": "vi",
    "two_factor_enabled": false
  }
}
​```

## 3. Field Definitions
| Field | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `auth.gmail` | String | Email dùng để định danh | Yes |
| `storage.used_space` | Long | Dung lượng đã dùng (bytes) | Yes |