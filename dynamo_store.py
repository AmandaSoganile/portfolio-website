import os
from datetime import date, datetime, timezone
from uuid import uuid4

import boto3

TABLE_NAME = os.environ.get("DYNAMO_TABLE", "amanda-portfolio")


class DynamoStore:
    def __init__(self):
        self._table = boto3.resource(
            "dynamodb", region_name="us-east-1"
        ).Table(TABLE_NAME)

    def _new_id(self):
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        return f"{ts}_{uuid4().hex[:8]}"

    # --- Reactions ---

    def add_reaction(self, fact_id: int, emoji: str) -> dict:
        self._table.update_item(
            Key={"pk": f"REACTION#{fact_id}", "sk": emoji},
            UpdateExpression="ADD #c :inc",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":inc": 1},
        )
        return self.get_reactions(fact_id)

    def get_reactions(self, fact_id: int) -> dict:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": f"REACTION#{fact_id}"},
        )
        return {item["sk"]: int(item["count"]) for item in resp["Items"]}

    # --- Books ---

    def add_book(self, name: str, title: str, author: str = "") -> None:
        self._table.put_item(Item={
            "pk": "BOOK",
            "sk": self._new_id(),
            "name": name,
            "title": title,
            "author": author,
            "submitted_at": date.today().isoformat(),
            "visible": 1,
        })

    def get_book_submissions(self) -> list:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": "BOOK"},
        )
        return [
            {"name": i["name"], "title": i["title"],
             "author": i.get("author", ""), "submitted_at": i["submitted_at"]}
            for i in resp["Items"] if i.get("visible", 1)
        ]

    def get_all_books(self) -> list:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": "BOOK"},
        )
        return [
            {"id": i["sk"], "name": i["name"], "title": i["title"],
             "author": i.get("author", ""), "submitted_at": i["submitted_at"],
             "visible": int(i.get("visible", 1))}
            for i in resp["Items"]
        ]

    def toggle_book_visible(self, row_id) -> None:
        item = self._table.get_item(
            Key={"pk": "BOOK", "sk": str(row_id)}
        ).get("Item")
        if item:
            self._table.update_item(
                Key={"pk": "BOOK", "sk": str(row_id)},
                UpdateExpression="SET visible = :v",
                ExpressionAttributeValues={
                    ":v": 0 if item.get("visible", 1) else 1
                },
            )

    def delete_book(self, row_id) -> None:
        self._table.delete_item(Key={"pk": "BOOK", "sk": str(row_id)})

    # --- Songs ---

    def add_song(self, name: str, title: str, artist: str = "",
                 note: str = "") -> None:
        self._table.put_item(Item={
            "pk": "SONG",
            "sk": self._new_id(),
            "name": name,
            "title": title,
            "artist": artist,
            "note": note,
            "submitted_at": date.today().isoformat(),
            "visible": 1,
        })

    def get_song_submissions(self) -> list:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": "SONG"},
        )
        return [
            {"name": i["name"], "title": i["title"],
             "artist": i.get("artist", ""), "note": i.get("note", ""),
             "submitted_at": i["submitted_at"]}
            for i in resp["Items"] if i.get("visible", 1)
        ]

    def get_all_songs(self) -> list:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": "SONG"},
        )
        return [
            {"id": i["sk"], "name": i["name"], "title": i["title"],
             "artist": i.get("artist", ""), "note": i.get("note", ""),
             "submitted_at": i["submitted_at"],
             "visible": int(i.get("visible", 1))}
            for i in resp["Items"]
        ]

    def toggle_song_visible(self, row_id) -> None:
        item = self._table.get_item(
            Key={"pk": "SONG", "sk": str(row_id)}
        ).get("Item")
        if item:
            self._table.update_item(
                Key={"pk": "SONG", "sk": str(row_id)},
                UpdateExpression="SET visible = :v",
                ExpressionAttributeValues={
                    ":v": 0 if item.get("visible", 1) else 1
                },
            )

    def delete_song(self, row_id) -> None:
        self._table.delete_item(Key={"pk": "SONG", "sk": str(row_id)})

    # --- Contact Messages ---

    def add_contact_message(self, name: str, email: str,
                            message: str) -> None:
        self._table.put_item(Item={
            "pk": "MESSAGE",
            "sk": self._new_id(),
            "name": name,
            "email": email,
            "message": message,
            "received_at": datetime.now(timezone.utc).isoformat(),
        })

    def get_contact_messages(self) -> list:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": "MESSAGE"},
            ScanIndexForward=False,
        )
        return [
            {"id": i["sk"], "name": i["name"], "email": i["email"],
             "message": i["message"], "received_at": i["received_at"]}
            for i in resp["Items"]
        ]

    def delete_contact_message(self, row_id) -> None:
        self._table.delete_item(Key={"pk": "MESSAGE", "sk": str(row_id)})

    # --- Page Views ---

    def record_page_view(self, path: str, ip_hash: str,
                         country: str = "", city: str = "",
                         region: str = "") -> None:
        now = datetime.now(timezone.utc).isoformat()
        self._table.put_item(Item={
            "pk": "PAGEVIEW",
            "sk": self._new_id(),
            "path": path,
            "visited_at": now,
            "ip_hash": ip_hash,
            "country": country,
            "city": city,
            "region": region,
        })
        self._table.update_item(
            Key={"pk": "VISITOR", "sk": ip_hash},
            UpdateExpression="SET country = :c, city = :ci, #r = :r,"
                            " last_seen = :ls ADD view_count :inc",
            ExpressionAttributeNames={"#r": "region"},
            ExpressionAttributeValues={
                ":c": country, ":ci": city, ":r": region,
                ":ls": now, ":inc": 1,
            },
        )

    def get_known_ip_location(self, ip_hash: str):
        item = self._table.get_item(
            Key={"pk": "VISITOR", "sk": ip_hash}
        ).get("Item")
        if item and item.get("country"):
            return {
                "country": item["country"],
                "city": item.get("city", ""),
                "region": item.get("region", ""),
            }
        return None

    def get_visitor_stats(self) -> dict:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": "VISITOR"},
            ProjectionExpression="view_count",
        )
        items = resp["Items"]
        total = sum(int(i.get("view_count", 0)) for i in items)
        return {"total_views": total, "unique_visitors": len(items)}

    def get_visitor_locations(self) -> list:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": "VISITOR"},
        )
        locations: dict[tuple, dict] = {}
        for item in resp["Items"]:
            country = item.get("country", "")
            if not country:
                continue
            city = item.get("city", "")
            region = item.get("region", "")
            key = (country, city, region)
            if key not in locations:
                locations[key] = {
                    "country": country, "city": city, "region": region,
                    "visitors": 0, "views": 0,
                }
            locations[key]["visitors"] += 1
            locations[key]["views"] += int(item.get("view_count", 0))
        return sorted(locations.values(), key=lambda x: x["visitors"],
                      reverse=True)

    def get_recent_visits(self, limit: int = 50) -> list:
        resp = self._table.query(
            KeyConditionExpression="pk = :pk",
            ExpressionAttributeValues={":pk": "PAGEVIEW"},
            ScanIndexForward=False,
            Limit=limit,
        )
        return [
            {"path": i["path"], "visited_at": i["visited_at"],
             "country": i.get("country", ""), "city": i.get("city", ""),
             "region": i.get("region", "")}
            for i in resp["Items"]
        ]
