"""
Server Administration System for RPG AI
Handles server management, data reset, and administrative commands
"""
from typing import Dict, List, Optional, Any
import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from ..utils.logger import logger
from ..utils.config import config

class ServerAdmin:
    """Handles server administration and data management"""
    
    def __init__(self):
        self.admin_commands = self._load_admin_commands()
        self.backup_directory = Path("backups")
        self.saves_directory = Path("saves")
        self.logs_directory = Path("logs")
        
        # Create necessary directories
        self.backup_directory.mkdir(exist_ok=True)
        self.saves_directory.mkdir(exist_ok=True)
        self.logs_directory.mkdir(exist_ok=True)
        
        logger.info("Server Administration System initialized")
    
    def _load_admin_commands(self) -> Dict[str, Dict]:
        """Load available administrative commands"""
        return {
            'reiniciar': {
                'description': 'Reinicia o servidor completamente',
                'permission': 'admin',
                'danger_level': 'medium',
                'requires_confirmation': True
            },
            'deletar_dados': {
                'description': 'Deleta todos os dados do servidor',
                'permission': 'admin',
                'danger_level': 'high',
                'requires_confirmation': True
            },
            'backup': {
                'description': 'Cria backup de todos os dados',
                'permission': 'admin',
                'danger_level': 'low',
                'requires_confirmation': False
            },
            'restaurar': {
                'description': 'Restaura dados de um backup',
                'permission': 'admin',
                'danger_level': 'medium',
                'requires_confirmation': True
            },
            'limpar_logs': {
                'description': 'Limpa logs antigos',
                'permission': 'admin',
                'danger_level': 'low',
                'requires_confirmation': False
            },
            'status_servidor': {
                'description': 'Mostra status detalhado do servidor',
                'permission': 'admin',
                'danger_level': 'none',
                'requires_confirmation': False
            },
            'manutencao': {
                'description': 'Coloca servidor em modo manutenção',
                'permission': 'admin',
                'danger_level': 'medium',
                'requires_confirmation': True
            }
        }
    
    def execute_admin_command(self, command: str, parameters: List[str] = None, admin_level: str = 'user') -> Dict[str, Any]:
        """Execute an administrative command"""
        
        if command not in self.admin_commands:
            return {
                'success': False,
                'message': f'Comando administrativo desconhecido: {command}',
                'available_commands': list(self.admin_commands.keys())
            }
        
        command_info = self.admin_commands[command]
        
        # Check permissions
        if admin_level != 'admin' and command_info['permission'] == 'admin':
            return {
                'success': False,
                'message': 'Permissão insuficiente para executar este comando',
                'required_permission': command_info['permission']
            }
        
        # Execute command
        try:
            if command == 'reiniciar':
                result = self._restart_server(parameters)
            elif command == 'deletar_dados':
                result = self._delete_all_data(parameters)
            elif command == 'backup':
                result = self._create_backup(parameters)
            elif command == 'restaurar':
                result = self._restore_backup(parameters)
            elif command == 'limpar_logs':
                result = self._clean_logs(parameters)
            elif command == 'status_servidor':
                result = self._get_server_status(parameters)
            elif command == 'manutencao':
                result = self._maintenance_mode(parameters)
            else:
                result = {
                    'success': False,
                    'message': f'Comando {command} não implementado'
                }
            
            # Add command metadata
            result.update({
                'command': command,
                'executed_at': datetime.now().isoformat(),
                'admin_level': admin_level,
                'danger_level': command_info['danger_level']
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing admin command {command}: {e}")
            return {
                'success': False,
                'message': f'Erro ao executar comando {command}: {str(e)}',
                'command': command,
                'error': str(e)
            }
    
    def _restart_server(self, parameters: List[str] = None) -> Dict[str, Any]:
        """Restart the server completely"""
        
        logger.warning("Server restart requested by admin")
        
        # Create backup before restart
        backup_result = self._create_backup(['pre_restart'])
        
        # Save current server state
        server_state = {
            'restart_requested': True,
            'restart_timestamp': datetime.now().isoformat(),
            'backup_created': backup_result['success'],
            'backup_file': backup_result.get('backup_file', 'unknown')
        }
        
        # Save restart state
        restart_file = Path("server_restart_state.json")
        with open(restart_file, 'w', encoding='utf-8') as f:
            json.dump(server_state, f, indent=2, ensure_ascii=False)
        
        return {
            'success': True,
            'message': 'Servidor será reiniciado. Backup criado antes da reinicialização.',
            'backup_result': backup_result,
            'restart_state_file': str(restart_file),
            'next_steps': [
                'Servidor será encerrado',
                'Todos os dados serão preservados',
                'Servidor será reiniciado automaticamente',
                'Jogadores precisarão reconectar'
            ]
        }
    
    def _delete_all_data(self, parameters: List[str] = None) -> Dict[str, Any]:
        """Delete all server data"""
        
        logger.critical("Complete data deletion requested by admin")
        
        # Create final backup before deletion
        backup_result = self._create_backup(['pre_deletion'])
        
        # List all data that will be deleted
        data_to_delete = []
        
        # Saves directory
        if self.saves_directory.exists():
            for save_file in self.saves_directory.glob("*.json"):
                data_to_delete.append(str(save_file))
        
        # Logs directory
        if self.logs_directory.exists():
            for log_file in self.logs_directory.glob("*.log"):
                data_to_delete.append(str(log_file))
        
        # Other data files
        other_files = [
            "server_restart_state.json",
            "campaign_state.json",
            "npc_memories.json"
        ]
        
        for file_path in other_files:
            if Path(file_path).exists():
                data_to_delete.append(file_path)
        
        # Delete data
        deleted_count = 0
        for file_path in data_to_delete:
            try:
                Path(file_path).unlink()
                deleted_count += 1
                logger.info(f"Deleted: {file_path}")
            except Exception as e:
                logger.error(f"Failed to delete {file_path}: {e}")
        
        # Clear directories (but keep them)
        for directory in [self.saves_directory, self.logs_directory]:
            if directory.exists():
                for item in directory.iterdir():
                    if item.is_file():
                        try:
                            item.unlink()
                            deleted_count += 1
                        except Exception as e:
                            logger.error(f"Failed to delete {item}: {e}")
        
        return {
            'success': True,
            'message': f'Todos os dados do servidor foram deletados. {deleted_count} arquivos removidos.',
            'backup_created': backup_result['success'],
            'backup_file': backup_result.get('backup_file', 'unknown'),
            'files_deleted': deleted_count,
            'data_directories_cleared': [
                str(self.saves_directory),
                str(self.logs_directory)
            ],
            'warning': 'Esta ação é irreversível! Use o backup se necessário.'
        }
    
    def _create_backup(self, parameters: List[str] = None) -> Dict[str, Any]:
        """Create a backup of all server data"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        
        if parameters and parameters[0]:
            backup_name = f"backup_{parameters[0]}_{timestamp}"
        
        backup_path = self.backup_directory / backup_name
        backup_path.mkdir(exist_ok=True)
        
        # Backup saves
        saves_backup = backup_path / "saves"
        saves_backup.mkdir(exist_ok=True)
        
        if self.saves_directory.exists():
            for save_file in self.saves_directory.glob("*.json"):
                try:
                    shutil.copy2(save_file, saves_backup / save_file.name)
                except Exception as e:
                    logger.error(f"Failed to backup save file {save_file}: {e}")
        
        # Backup logs
        logs_backup = backup_path / "logs"
        logs_backup.mkdir(exist_ok=True)
        
        if self.logs_directory.exists():
            for log_file in self.logs_directory.glob("*.log"):
                try:
                    shutil.copy2(log_file, logs_backup / log_file.name)
                except Exception as e:
                    logger.error(f"Failed to backup log file {log_file}: {e}")
        
        # Backup other important files
        other_files = [
            "server_restart_state.json",
            "campaign_state.json",
            "npc_memories.json"
        ]
        
        for file_path in other_files:
            if Path(file_path).exists():
                try:
                    shutil.copy2(file_path, backup_path / file_path)
                except Exception as e:
                    logger.error(f"Failed to backup {file_path}: {e}")
        
        # Create backup manifest
        manifest = {
            'backup_name': backup_name,
            'created_at': datetime.now().isoformat(),
            'backup_type': 'full_server_backup',
            'parameters': parameters or [],
            'files_backed_up': len(list(backup_path.rglob("*")))
        }
        
        manifest_file = backup_path / "backup_manifest.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Backup created: {backup_path}")
        
        return {
            'success': True,
            'message': f'Backup criado com sucesso: {backup_name}',
            'backup_path': str(backup_path),
            'backup_file': backup_name,
            'files_backed_up': manifest['files_backed_up'],
            'backup_size': self._get_directory_size(backup_path)
        }
    
    def _restore_backup(self, parameters: List[str] = None) -> Dict[str, Any]:
        """Restore data from a backup"""
        
        if not parameters or not parameters[0]:
            return {
                'success': False,
                'message': 'Nome do backup deve ser especificado'
            }
        
        backup_name = parameters[0]
        backup_path = self.backup_directory / backup_name
        
        if not backup_path.exists():
            return {
                'success': False,
                'message': f'Backup {backup_name} não encontrado'
            }
        
        # Verify backup integrity
        manifest_file = backup_path / "backup_manifest.json"
        if not manifest_file.exists():
            return {
                'success': False,
                'message': f'Backup {backup_name} corrompido (manifesto não encontrado)'
            }
        
        try:
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except Exception as e:
            return {
                'success': False,
                'message': f'Erro ao ler manifesto do backup: {e}'
            }
        
        # Create backup of current state before restoration
        current_backup = self._create_backup(['pre_restore'])
        
        # Restore data
        restored_count = 0
        
        # Restore saves
        saves_backup = backup_path / "saves"
        if saves_backup.exists():
            for save_file in saves_backup.glob("*.json"):
                try:
                    shutil.copy2(save_file, self.saves_directory / save_file.name)
                    restored_count += 1
                except Exception as e:
                    logger.error(f"Failed to restore save file {save_file}: {e}")
        
        # Restore logs
        logs_backup = backup_path / "logs"
        if logs_backup.exists():
            for log_file in logs_backup.glob("*.log"):
                try:
                    shutil.copy2(log_file, self.logs_directory / log_file.name)
                    restored_count += 1
                except Exception as e:
                    logger.error(f"Failed to restore log file {log_file}: {e}")
        
        # Restore other files
        for file_path in ["server_restart_state.json", "campaign_state.json", "npc_memories.json"]:
            backup_file = backup_path / file_path
            if backup_file.exists():
                try:
                    shutil.copy2(backup_file, file_path)
                    restored_count += 1
                except Exception as e:
                    logger.error(f"Failed to restore {file_path}: {e}")
        
        logger.info(f"Backup restored: {backup_name} ({restored_count} files)")
        
        return {
            'success': True,
            'message': f'Backup {backup_name} restaurado com sucesso',
            'backup_name': backup_name,
            'files_restored': restored_count,
            'current_backup_created': current_backup['success'],
            'restoration_timestamp': datetime.now().isoformat()
        }
    
    def _clean_logs(self, parameters: List[str] = None) -> Dict[str, Any]:
        """Clean old log files"""
        
        if not self.logs_directory.exists():
            return {
                'success': True,
                'message': 'Diretório de logs não existe',
                'files_cleaned': 0
            }
        
        # Get log retention days from parameters or config
        retention_days = 7  # Default
        if parameters and parameters[0].isdigit():
            retention_days = int(parameters[0])
        
        cutoff_date = datetime.now().timestamp() - (retention_days * 24 * 3600)
        
        cleaned_count = 0
        for log_file in self.logs_directory.glob("*.log"):
            try:
                if log_file.stat().st_mtime < cutoff_date:
                    log_file.unlink()
                    cleaned_count += 1
            except Exception as e:
                logger.error(f"Failed to clean log file {log_file}: {e}")
        
        return {
            'success': True,
            'message': f'Logs antigos (mais de {retention_days} dias) foram limpos',
            'files_cleaned': cleaned_count,
            'retention_days': retention_days
        }
    
    def _get_server_status(self, parameters: List[str] = None) -> Dict[str, Any]:
        """Get detailed server status"""
        
        # Get directory sizes
        saves_size = self._get_directory_size(self.saves_directory)
        logs_size = self._get_directory_size(self.logs_directory)
        backups_size = self._get_directory_size(self.backup_directory)
        
        # Count files
        saves_count = len(list(self.saves_directory.glob("*.json"))) if self.saves_directory.exists() else 0
        logs_count = len(list(self.logs_directory.glob("*.log"))) if self.logs_directory.exists() else 0
        backups_count = len(list(self.backup_directory.glob("backup_*"))) if self.backup_directory.exists() else 0
        
        # Check for important files
        important_files = {
            'server_restart_state.json': Path("server_restart_state.json").exists(),
            'campaign_state.json': Path("campaign_state.json").exists(),
            'npc_memories.json': Path("npc_memories.json").exists()
        }
        
        return {
            'success': True,
            'message': 'Status do servidor obtido com sucesso',
            'server_status': {
                'directories': {
                    'saves': {
                        'path': str(self.saves_directory),
                        'size': saves_size,
                        'file_count': saves_count
                    },
                    'logs': {
                        'path': str(self.logs_directory),
                        'size': logs_size,
                        'file_count': logs_count
                    },
                    'backups': {
                        'path': str(self.backup_directory),
                        'size': backups_size,
                        'backup_count': backups_count
                    }
                },
                'important_files': important_files,
                'total_data_size': saves_size + logs_size + backups_size,
                'last_backup': self._get_last_backup_info()
            }
        }
    
    def _maintenance_mode(self, parameters: List[str] = None) -> Dict[str, Any]:
        """Put server in maintenance mode"""
        
        maintenance_state = {
            'maintenance_mode': True,
            'activated_at': datetime.now().isoformat(),
            'activated_by': 'admin',
            'reason': parameters[0] if parameters else 'Manutenção programada',
            'estimated_duration': parameters[1] if len(parameters) > 1 else 'Indefinido'
        }
        
        # Save maintenance state
        maintenance_file = Path("maintenance_state.json")
        with open(maintenance_file, 'w', encoding='utf-8') as f:
            json.dump(maintenance_state, f, indent=2, ensure_ascii=False)
        
        logger.warning(f"Server put in maintenance mode: {maintenance_state['reason']}")
        
        return {
            'success': True,
            'message': 'Servidor colocado em modo manutenção',
            'maintenance_state': maintenance_state,
            'effects': [
                'Novas conexões serão rejeitadas',
                'Jogadores existentes serão desconectados',
                'Sistema será reiniciado após manutenção'
            ]
        }
    
    def _get_directory_size(self, directory: Path) -> str:
        """Get the size of a directory in human-readable format"""
        if not directory.exists():
            return "0 B"
        
        total_size = 0
        try:
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            return "Unknown"
        
        # Convert to human-readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if total_size < 1024.0:
                return f"{total_size:.1f} {unit}"
            total_size /= 1024.0
        
        return f"{total_size:.1f} TB"
    
    def _get_last_backup_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the last backup"""
        if not self.backup_directory.exists():
            return None
        
        backup_dirs = [d for d in self.backup_directory.iterdir() if d.is_dir() and d.name.startswith('backup_')]
        if not backup_dirs:
            return None
        
        # Get the most recent backup
        latest_backup = max(backup_dirs, key=lambda d: d.stat().st_mtime)
        manifest_file = latest_backup / "backup_manifest.json"
        
        if manifest_file.exists():
            try:
                with open(manifest_file, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                return {
                    'name': manifest.get('backup_name', latest_backup.name),
                    'created_at': manifest.get('created_at', 'Unknown'),
                    'size': self._get_directory_size(latest_backup)
                }
            except Exception:
                pass
        
        return {
            'name': latest_backup.name,
            'created_at': 'Unknown',
            'size': self._get_directory_size(latest_backup)
        }
    
    def get_available_commands(self, admin_level: str = 'user') -> List[Dict[str, Any]]:
        """Get list of available administrative commands"""
        commands = []
        
        for cmd_name, cmd_info in self.admin_commands.items():
            if admin_level == 'admin' or cmd_info['permission'] != 'admin':
                commands.append({
                    'command': cmd_name,
                    'description': cmd_info['description'],
                    'permission': cmd_info['permission'],
                    'danger_level': cmd_info['danger_level'],
                    'requires_confirmation': cmd_info['requires_confirmation']
                })
        
        return commands
    
    def shutdown(self) -> None:
        """Shutdown the administration system"""
        logger.info("Server Administration System shutting down")
        
        # Create final status report
        status = self._get_server_status()
        logger.info(f"Final server status: {status}")
