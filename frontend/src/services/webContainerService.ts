import { WebContainer } from '@webcontainer/api';
import { ProjectConfig } from '../types/chat';

interface PackageJson {
    name: string;
    type: string;
    version: string;
    dependencies?: Record<string, string>;
    devDependencies?: Record<string, string>;
}

class WebContainerService {
    private static instance: WebContainerService;
    private webcontainerInstance: WebContainer | null = null;
    private mountedFiles: Set<string> = new Set();

    private constructor() {}

    static getInstance(): WebContainerService {
        if (!WebContainerService.instance) {
            WebContainerService.instance = new WebContainerService();
        }
        return WebContainerService.instance;
    }

    async initialize(): Promise<void> {
        if (!this.webcontainerInstance) {
            this.webcontainerInstance = await WebContainer.boot();
        }
    }

    async createProject(config: ProjectConfig): Promise<void> {
        if (!this.webcontainerInstance) {
            throw new Error('WebContainer not initialized');
        }

        // Create package.json
        const packageJson: PackageJson = {
            name: config.name,
            type: config.type,
            version: '1.0.0',
            dependencies: config.dependencies?.reduce<Record<string, string>>((acc, dep) => ({ ...acc, [dep]: 'latest' }), {}),
            devDependencies: config.devDependencies?.reduce<Record<string, string>>((acc, dep) => ({ ...acc, [dep]: 'latest' }), {})
        };

        await this.webcontainerInstance.mount({
            'package.json': {
                file: {
                    contents: JSON.stringify(packageJson, null, 2)
                }
            }
        });

        // Install dependencies
        const install = await this.webcontainerInstance.spawn('npm', ['install']);
        const installProcess = await install.exit;

        if (installProcess !== 0) {
            throw new Error('Failed to install dependencies');
        }
    }

    async writeFile(path: string, contents: string): Promise<void> {
        if (!this.webcontainerInstance) {
            throw new Error('WebContainer not initialized');
        }

        const files = path.split('/').reduce<Record<string, any>>((acc, part, index, array) => {
            if (index === array.length - 1) {
                return {
                    ...acc,
                    [part]: {
                        file: {
                            contents
                        }
                    }
                };
            }
            return {
                ...acc,
                [part]: {
                    directory: {}
                }
            };
        }, {});

        await this.webcontainerInstance.mount(files);
        this.mountedFiles.add(path);
    }

    async readFile(path: string): Promise<string> {
        if (!this.webcontainerInstance) {
            throw new Error('WebContainer not initialized');
        }

        const file = await this.webcontainerInstance.fs.readFile(path, 'utf-8');
        return file;
    }

    async runCommand(command: string, args: string[] = []): Promise<{ exitCode: number; output: string }> {
        if (!this.webcontainerInstance) {
            throw new Error('WebContainer not initialized');
        }

        const process = await this.webcontainerInstance.spawn(command, args);
        const output: string[] = [];

        process.output.pipeTo(new WritableStream({
            write(data) {
                output.push(data);
            }
        }));

        const exitCode = await process.exit;
        return {
            exitCode,
            output: output.join('\n')
        };
    }

    async startDevServer(command: string = 'npm', args: string[] = ['run', 'dev']): Promise<number> {
        if (!this.webcontainerInstance) {
            throw new Error('WebContainer not initialized');
        }

        const process = await this.webcontainerInstance.spawn(command, args);
        return process.exit;
    }
}

export const webContainerService = WebContainerService.getInstance();
