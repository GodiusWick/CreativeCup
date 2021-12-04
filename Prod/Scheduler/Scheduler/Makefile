migrationup:
	migrate -path migration -database "postgresql://rosatom:@myp3a.noip.me:5432/rosatom?sslmode=disable" -verbose up

migrationdown:
	migrate -path migration -database "postgresql://rosatom:@myp3a.noip.me:5432/rosatom?sslmode=disable" -verbose down

PHONY: migrationup migrationdown