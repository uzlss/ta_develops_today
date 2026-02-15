from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.tables.project import Project
from src.tables.project_place import ProjectPlace


class DBService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # --- Projects ---

    async def get_projects(self) -> list[Project]:
        result = await self.db.execute(
            select(Project)
            .options(selectinload(Project.places))
            .order_by(Project.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_project(self, project_id: int) -> Project | None:
        result = await self.db.execute(
            select(Project)
            .options(selectinload(Project.places))
            .where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def create_project(
        self,
        name: str,
        description: str | None,
        start_date,
        places_data: list[dict],
    ) -> Project:
        project = Project(
            name=name, description=description, start_date=start_date
        )
        for place in places_data:
            project.places.append(ProjectPlace(**place))
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project, attribute_names=["places"])
        return project

    async def update_project(self, project: Project, data: dict) -> Project:
        for key, val in data.items():
            if val is not None:
                setattr(project, key, val)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete_project(self, project: Project) -> None:
        await self.db.delete(project)

    # --- Places ---

    async def get_places(self, project_id: int) -> list[ProjectPlace]:
        result = await self.db.execute(
            select(ProjectPlace)
            .where(ProjectPlace.project_id == project_id)
            .order_by(ProjectPlace.created_at)
        )
        return list(result.scalars().all())

    async def get_place(
        self, project_id: int, place_id: int
    ) -> ProjectPlace | None:
        result = await self.db.execute(
            select(ProjectPlace).where(
                ProjectPlace.project_id == project_id,
                ProjectPlace.id == place_id,
            )
        )
        return result.scalar_one_or_none()

    async def add_place(self, project_id: int, data: dict) -> ProjectPlace:
        place = ProjectPlace(project_id=project_id, **data)
        self.db.add(place)
        await self.db.flush()
        await self.db.refresh(place)
        return place

    async def count_places(self, project_id: int) -> int:
        result = await self.db.execute(
            select(func.count(ProjectPlace.id)).where(
                ProjectPlace.project_id == project_id
            )
        )
        return result.scalar()

    async def place_exists(
        self, project_id: int, external_id: int
    ) -> bool:
        result = await self.db.execute(
            select(ProjectPlace.id).where(
                ProjectPlace.project_id == project_id,
                ProjectPlace.external_id == external_id,
            )
        )
        return result.scalar_one_or_none() is not None

    async def update_place(
        self, place: ProjectPlace, data: dict
    ) -> ProjectPlace:
        for key, val in data.items():
            if val is not None:
                setattr(place, key, val)
        await self.db.flush()
        await self.db.refresh(place)
        return place
