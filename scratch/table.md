# 레거시 PHP 파일 전수 분석 보고서 (1:1 매핑)

## 1. 인증 및 세션 관련 파일

| 파일명 | 크기 (Bytes) | 주요 테이블 | 역할/주석 타이틀 |
|---|---|---|---|
| [connect.php](file:///f:/pe/public_html/test-migration/sitepro/connect.php) | 36,892 | tb_keys_remote_devices, tb_login, tb_reminder_other, tb_reminder_vehicle, tb_tasks, tb_tasks_employees_affectation | CONNECT |
| [destroysession.php](file:///f:/pe/public_html/test-migration/sitepro/destroysession.php) | 626 |  |  |
| [disconnect.php](file:///f:/pe/public_html/test-migration/sitepro/disconnect.php) | 2,459 | tb_keys_remote_devices, tb_login | DISCONNECT |
| [register.php](file:///f:/pe/public_html/test-migration/sitepro/register.php) | 7,731 | tb_keys_remote_devices, tb_login | REGISTER |

## 2. 메인 페이지 및 라우팅 허브

| 파일명 | 크기 (Bytes) | 주요 테이블 | 역할/주석 타이틀 |
|---|---|---|---|
| [1.php](file:///f:/pe/public_html/test-migration/sitepro/1.php) | 9,614 | tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [2.php](file:///f:/pe/public_html/test-migration/sitepro/2.php) | 259,282 | date_creation, tb_jobs, tb_keys_remote_devices, tb_login, tb_week_notes | Facebook Open Graph |
| [3.php](file:///f:/pe/public_html/test-migration/sitepro/3.php) | 124,788 | date_creation, tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [4.php](file:///f:/pe/public_html/test-migration/sitepro/4.php) | 38,702 | tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [5.php](file:///f:/pe/public_html/test-migration/sitepro/5.php) | 12,425 | tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [functions.inc.php](file:///f:/pe/public_html/test-migration/sitepro/functions.inc.php) | 25,883 | bots | \n$style\n |
| [index.php](file:///f:/pe/public_html/test-migration/sitepro/index.php) | 37,873 |  |  |

## 3. 주요 비즈니스 액션 및 API 처리 파일

| 파일명 | 크기 (Bytes) | 주요 테이블 | 역할/주석 타이틀 |
|---|---|---|---|
| [PunchSheetAction.php](file:///f:/pe/public_html/test-migration/sitepro/PunchSheetAction.php) | 19,806 | LIST, tb_jobs_date_install, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | PUNCH SHEET ACTION |
| [create_update_job.php](file:///f:/pe/public_html/test-migration/sitepro/create_update_job.php) | 36,226 | JOBS, date_creation, tb_jobs, tb_jobs_date_install, tb_jobs_dates, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_wip | CREATE OR UPDATE JOBS DEV |
| [update_dateinstalljobs.php](file:///f:/pe/public_html/test-migration/sitepro/update_dateinstalljobs.php) | 8,950 | tb_jobs, tb_jobs_date_install, tb_keys_remote_devices, tb_login | UPDATE DATE INSTALL JOB |
| [update_jobsdetails.php](file:///f:/pe/public_html/test-migration/sitepro/update_jobsdetails.php) | 91,047 | JOB, b, date_creation, tb_jobs, tb_jobs_date_install, tb_jobs_dates, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | UPDATE JOB DETAIL |

## 4. 개별 기능별 숫자 파일 (1.php ~ 73.php)

| 파일명 | 크기 (Bytes) | 주요 테이블 | 역할/주석 타이틀 |
|---|---|---|---|
| [10.php](file:///f:/pe/public_html/test-migration/sitepro/10.php) | 28,770 | tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |
| [11.php](file:///f:/pe/public_html/test-migration/sitepro/11.php) | 30,674 | tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [12.php](file:///f:/pe/public_html/test-migration/sitepro/12.php) | 7,919 | USER, tb_keys_remote_devices, tb_login | UPDATE USER |
| [13.php](file:///f:/pe/public_html/test-migration/sitepro/13.php) | 2,804 | tb_keys_remote_devices, tb_login | DELETE USER |
| [14.php](file:///f:/pe/public_html/test-migration/sitepro/14.php) | 2,891 | tb_keys_remote_devices, tb_login | RESET PASSWORD USER |
| [15.php](file:///f:/pe/public_html/test-migration/sitepro/15.php) | 121,406 | date_creation, finish_date_update, tb_jobs, tb_jobs_date_install, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |
| [16.php](file:///f:/pe/public_html/test-migration/sitepro/16.php) | 99,047 | echo, finished_date, here, tb_keys_remote_devices, tb_login, tb_tasks, tb_tasks_employees_affectation | Facebook Open Graph |
| [17.php](file:///f:/pe/public_html/test-migration/sitepro/17.php) | 239,874 | tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |
| [18.php](file:///f:/pe/public_html/test-migration/sitepro/18.php) | 2,737 | PASSWORD, tb_keys_remote_devices, tb_login | UPDATE PASSWORD |
| [19.php](file:///f:/pe/public_html/test-migration/sitepro/19.php) | 28,959 | date_creation, tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_wip | Facebook Open Graph |
| [20.php](file:///f:/pe/public_html/test-migration/sitepro/20.php) | 55,209 | echo, tb_keys_remote_devices, tb_login, tb_reminder_other, tb_reminder_vehicle | Facebook Open Graph |
| [21.php](file:///f:/pe/public_html/test-migration/sitepro/21.php) | 5,161 | REMINDER, tb_keys_remote_devices, tb_login, tb_reminder_vehicle | UPDATE REMINDER VEHICLES |
| [22.php](file:///f:/pe/public_html/test-migration/sitepro/22.php) | 2,777 | tb_keys_remote_devices, tb_login, tb_reminder_vehicle | DELETE VEHICLE |
| [23.php](file:///f:/pe/public_html/test-migration/sitepro/23.php) | 4,114 | tb_keys_remote_devices, tb_login, tb_reminder_vehicle | CREATE VEHICLES |
| [24.php](file:///f:/pe/public_html/test-migration/sitepro/24.php) | 4,922 | REMINDER, tb_keys_remote_devices, tb_login | UPDATE REMINDER SITESAFE |
| [25.php](file:///f:/pe/public_html/test-migration/sitepro/25.php) | 4,089 | REMINDER, tb_keys_remote_devices, tb_login, tb_reminder_other | UPDATE REMINDER OTHERS |
| [26.php](file:///f:/pe/public_html/test-migration/sitepro/26.php) | 2,759 | tb_keys_remote_devices, tb_login, tb_reminder_other | DELETE OTHER |
| [27.php](file:///f:/pe/public_html/test-migration/sitepro/27.php) | 3,457 | tb_keys_remote_devices, tb_login, tb_reminder_other | CREATE OTHER |
| [28.php](file:///f:/pe/public_html/test-migration/sitepro/28.php) | 8,927 | TASKS, on, tb_keys_remote_devices, tb_login, tb_tasks, tb_tasks_employees_affectation | UPDATE TASKS |
| [29.php](file:///f:/pe/public_html/test-migration/sitepro/29.php) | 3,245 | tb_keys_remote_devices, tb_login, tb_tasks, tb_tasks_employees_affectation | DELETE TASKS |
| [2bis.php](file:///f:/pe/public_html/test-migration/sitepro/2bis.php) | 135,132 | tb_jobs, tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [30.php](file:///f:/pe/public_html/test-migration/sitepro/30.php) | 7,674 | tb_keys_remote_devices, tb_login, tb_tasks, tb_tasks_employees_affectation | CREATE TASKS |
| [31.php](file:///f:/pe/public_html/test-migration/sitepro/31.php) | 4,352 | TASKS, tb_keys_remote_devices, tb_login, tb_tasks | UPDATE TASKS BY EMPLOYEE |
| [32.php](file:///f:/pe/public_html/test-migration/sitepro/32.php) | 79,288 | date_creation, document, tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_wip | Facebook Open Graph |
| [33.php](file:///f:/pe/public_html/test-migration/sitepro/33.php) | 4,827 | tb_keys_remote_devices, tb_login, tb_punchsheet | PUNCH SHEET ACTIONS |
| [34.php](file:///f:/pe/public_html/test-migration/sitepro/34.php) | 15,455 | echo, tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [35.php](file:///f:/pe/public_html/test-migration/sitepro/35.php) | 3,820 | DEVICE, query, tb_keys_remote_devices, tb_login | UPDATE DEVICE |
| [36.php](file:///f:/pe/public_html/test-migration/sitepro/36.php) | 3,324 | tb_keys_remote_devices, tb_login | CREATE DEVICE |
| [37.php](file:///f:/pe/public_html/test-migration/sitepro/37.php) | 2,772 | tb_keys_remote_devices, tb_login | DELETE DEVICE |
| [39.php](file:///f:/pe/public_html/test-migration/sitepro/39.php) | 68,460 | date_creation, tb_jobs, tb_jobs_date_install, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | TICK ALL JOBSHEET |
| [3bis.php](file:///f:/pe/public_html/test-migration/sitepro/3bis.php) | 58,517 | tb_jobs, tb_jobs_date_install, tb_jobs_details, tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [40.php](file:///f:/pe/public_html/test-migration/sitepro/40.php) | 19,404 | WIP, date_creation, if, tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_wip | UPDATE WIP DETAIL |
| [41.php](file:///f:/pe/public_html/test-migration/sitepro/41.php) | 5,146 | date_creation, tb_jobs, tb_keys_remote_devices, tb_login | WIP INSPECTION COMPLETED |
| [42.php](file:///f:/pe/public_html/test-migration/sitepro/42.php) | 51,642 | aray, drop, tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_leaves, tb_login, tb_public_holidays, tb_punchsheet | Facebook Open Graph |
| [43.php](file:///f:/pe/public_html/test-migration/sitepro/43.php) | 62,875 | date_start, date_stop, tb_keys_remote_devices, tb_leaves, tb_login, tb_public_holidays | Facebook Open Graph |
| [44.php](file:///f:/pe/public_html/test-migration/sitepro/44.php) | 3,829 | PUBLIC, tb_keys_remote_devices, tb_login, tb_public_holidays | UPDATE PUBLIC HOLIDAYS |
| [45.php](file:///f:/pe/public_html/test-migration/sitepro/45.php) | 4,195 | LEAVES, data, tb_keys_remote_devices, tb_leaves, tb_login | UPDATE LEAVES |
| [46.php](file:///f:/pe/public_html/test-migration/sitepro/46.php) | 3,432 | tb_keys_remote_devices, tb_login, tb_public_holidays | CREATE PUBLIC HOLIDAYS |
| [47.php](file:///f:/pe/public_html/test-migration/sitepro/47.php) | 3,488 | tb_keys_remote_devices, tb_leaves, tb_login | CREATE ANNUAL LEAVES |
| [48.php](file:///f:/pe/public_html/test-migration/sitepro/48.php) | 2,829 | tb_keys_remote_devices, tb_login, tb_public_holidays | DELETE PUBLIC HOLIDAYS |
| [49.php](file:///f:/pe/public_html/test-migration/sitepro/49.php) | 2,809 | tb_keys_remote_devices, tb_leaves, tb_login | DELETE ANNUAL LEAVES |
| [4bis.php](file:///f:/pe/public_html/test-migration/sitepro/4bis.php) | 49,821 | tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |
| [4bisSHOP.php](file:///f:/pe/public_html/test-migration/sitepro/4bisSHOP.php) | 42,266 | DESC, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |
| [50.php](file:///f:/pe/public_html/test-migration/sitepro/50.php) | 245,980 | b, date_creation, echo, tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |
| [51.php](file:///f:/pe/public_html/test-migration/sitepro/51.php) | 133,411 | tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |
| [52.php](file:///f:/pe/public_html/test-migration/sitepro/52.php) | 138,648 | tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | MODIFICATION OF PUNCH SHEET BY AN ADMIN DEV |
| [53.php](file:///f:/pe/public_html/test-migration/sitepro/53.php) | 17,354 | export_date, tb_export_data, tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [54.php](file:///f:/pe/public_html/test-migration/sitepro/54.php) | 3,637 | tb_export_data, tb_keys_remote_devices, tb_login | EXPORT DATABASE |
| [55.php](file:///f:/pe/public_html/test-migration/sitepro/55.php) | 3,372 | tb_keys_remote_devices, tb_login | EXPORT DATABASE |
| [56.php](file:///f:/pe/public_html/test-migration/sitepro/56.php) | 88,623 | tb_jobs, tb_jobs_date_install, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_production_plan, tb_public_holidays, var | Facebook Open Graph |
| [57.php](file:///f:/pe/public_html/test-migration/sitepro/57.php) | 5,436 | PRODUCTION, tb_keys_remote_devices, tb_login, tb_production_plan | UPDATE PRODUCTION PLAN |
| [58.php](file:///f:/pe/public_html/test-migration/sitepro/58.php) | 4,312 | tb_keys_remote_devices, tb_login, tb_production_plan | CREATE PRODUCTION PLAN |
| [59.php](file:///f:/pe/public_html/test-migration/sitepro/59.php) | 4,524 | tb_keys_remote_devices, tb_login, tb_production_plan | DELETE PRODUCTION PLAN |
| [6.php](file:///f:/pe/public_html/test-migration/sitepro/6.php) | 37,932 | here, tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [60.php](file:///f:/pe/public_html/test-migration/sitepro/60.php) | 21,224 | NOTES, tb_keys_remote_devices, tb_login, tb_week_notes | UPDATE NOTES ON WHITEBOARD |
| [61.php](file:///f:/pe/public_html/test-migration/sitepro/61.php) | 24,105 | tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [62.php](file:///f:/pe/public_html/test-migration/sitepro/62.php) | 5,123 | PAINTING, TICK, UNTICK, if, tb_jobs, tb_keys_remote_devices, tb_login | UPDATE PAINTING JOBS |
| [63.php](file:///f:/pe/public_html/test-migration/sitepro/63.php) | 3,071 | COMMENT, DB, tb_jobs, tb_keys_remote_devices, tb_login | UPDATE COMMENT PAINTING JOBS |
| [64.php](file:///f:/pe/public_html/test-migration/sitepro/64.php) | 40,486 | date_creation, tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [65.php](file:///f:/pe/public_html/test-migration/sitepro/65.php) | 4,550 | tb_jobs, tb_keys_remote_devices, tb_login | FASTENERS SAVE |
| [66.php](file:///f:/pe/public_html/test-migration/sitepro/66.php) | 17,264 | tb_keys_remote_devices, tb_login, tb_photos | Facebook Open Graph |
| [67.php](file:///f:/pe/public_html/test-migration/sitepro/67.php) | 8,548 | tb_keys_remote_devices, tb_login, tb_photos | UPLOAD PHOTO |
| [68.php](file:///f:/pe/public_html/test-migration/sitepro/68.php) | 3,785 | tb_keys_remote_devices, tb_login, tb_photos | OPEN PHOTO FULL SCREEN |
| [69.php](file:///f:/pe/public_html/test-migration/sitepro/69.php) | 3,363 | tb_keys_remote_devices, tb_login | ROTATE PHOTO |
| [7.php](file:///f:/pe/public_html/test-migration/sitepro/7.php) | 713,569 | Job, b, button, date_creation, echo, job, tb_jobs, tb_jobs_dates, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet, tb_wip | Facebook Open Graph |
| [70.php](file:///f:/pe/public_html/test-migration/sitepro/70.php) | 3,365 | tb_keys_remote_devices, tb_login | ROTATE PHOTO DEV |
| [71.php](file:///f:/pe/public_html/test-migration/sitepro/71.php) | 15,465 | tb_keys_remote_devices, tb_login | Facebook Open Graph |
| [72.php](file:///f:/pe/public_html/test-migration/sitepro/72.php) | 5,527 | tb_keys_remote_devices, tb_login |  |
| [73.php](file:///f:/pe/public_html/test-migration/sitepro/73.php) | 32,796 | tb_jobs_dates, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |
| [8.php](file:///f:/pe/public_html/test-migration/sitepro/8.php) | 64,350 | JOBSHEET, button, date_creation, echo, if, job, tb_jobs, tb_jobs_details, tb_keys_remote_devices, tb_login, value | Facebook Open Graph |
| [9.php](file:///f:/pe/public_html/test-migration/sitepro/9.php) | 266,613 | Punch_User, date_creation, tb_jobs_details, tb_keys_remote_devices, tb_login, tb_punchsheet | Facebook Open Graph |

