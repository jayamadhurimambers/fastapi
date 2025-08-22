import pytest
import asyncio
from asynwithpytest import task

class TestAsyncTasks:
    @pytest.mark.asyncio
    async def test_task_runs(self, capsys):
        await task("test", 0)
        captured = capsys.readouterr()
        assert "Task test started" in captured.out
        assert "Task test finished after 0 seconds" in captured.out